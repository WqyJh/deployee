import os
import sys
import uuid
import yaml
import click
import shutil
import subprocess
import pkg_resources

from . import __version__


def git_rev(repo):
    try:
        ret = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=repo)
        ret = ret.decode().strip()
        return ret
    except Exception as e:
        print(f'{repo} is not a git repo')



@click.command()
@click.version_option(__version__)
@click.argument('project') # Project path which should better be a git repo
@click.argument('stage', type=click.Choice(['test', 'staging', 'production']))
@click.option('-n', '--name', help='Project name. Default as the <project>.')
@click.option('--script', help='Custom test/run script. Default as "python manage.py test" or "gunicorn -c <gunicorn_conf> <wsgi_app>".')
@click.option('--framework', default='django', help='Run the framework specified tasks. For django is the migrations and static collection.')
@click.option('--gunicorn-conf', default='gunicorn.conf.py', help='Config filename for gunicorn relative to the project root path.')
@click.option('--wsgi-app', help='Gunicorn argument of wsgi application. Default as <project>.wsgi:application.')
@click.option('--postfix', help='Postfix which help avoiding conflict between the old code path and the new code path. default: value of `git rev-parse --short` if the project path is a git repo else "default".')
@click.option('--inventory', help='Ansible inventory file.')
@click.option('--parallel', is_flag=True, default=False, help='Run tests in parallel, only work for django test.')
@click.option('-d', '--debug', is_flag=True)
@click.option('-v', '--verbose', count=True, help='Verbosity for ansible-playbook.')
@click.option('--dry-run', is_flag=True, help='Print some arguments without real tasks running.')
def main(project, stage, name, script, framework, gunicorn_conf, wsgi_app, postfix, inventory, parallel, debug, verbose, dry_run):
    if inventory and not os.path.isfile(inventory):
        print(f'file "{inventory}" does not exist')
        sys.exit(1)

    project = os.path.abspath(project)
    name = name or os.path.basename(project)
    postfix = postfix or git_rev(project) or 'default'
    wsgi_app = wsgi_app or f'{name}.wsgi:application'

    vars = {
        'project_name': name,
        'stage': stage,
        'project_src': project,
        'gunicorn_conf': gunicorn_conf,
        'wsgi_app': wsgi_app,
        'postfix': postfix,
        'framework': framework,
        'django_test_command': 'test --parallel' if parallel else 'test',
    }

    if script:
        vars['script'] = script

    if dry_run:
        print(vars)
        sys.exit(0)

    if debug:
        print(vars)

    owd = os.getcwd()
    wd = f'deployee-{uuid.uuid4()}'

    src = pkg_resources.resource_filename('deployee', 'ansible')
    shutil.copytree(src, wd)

    if inventory:
        shutil.copy(inventory, wd)

    os.chdir(wd)

    with open('vars.yml', 'w') as f:
        f.write(yaml.dump(vars))

    commands = ['ansible-playbook', 'playbook.yml']
    if verbose:
        commands.append('-' + verbose * 'v')

    ret = subprocess.call(commands)

    os.chdir(owd)
    shutil.rmtree(wd)

    sys.exit(ret)


if __name__ == '__main__':
    main()
