import os
import sys
import uuid
import yaml
import click
import shutil
import subprocess

from . import __version__


def git_rev(repo):
    try:
        ret = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=repo)
        ret = ret.decode().strip()
        return ret
    except Exception as e:
        print(f'{repo} is not a git repo')



@click.command()
@click.argument('project')
@click.argument('stage', type=click.Choice(['test', 'staging', 'production']))
@click.option('-n', '--name')
@click.option('--gunicorn-conf', default='gunicorn.conf.py')
@click.option('--wsgi-app')
@click.option('--postfix')
@click.option('-d', '--debug', is_flag=True)
@click.option('-v', '--verbose', count=True)
@click.option('--dry-run', is_flag=True)
def main(project, stage, name=None, gunicorn_conf=None, wsgi_app=None, postfix=None, debug=False, verbose=0, dry_run=False):
    project = os.path.abspath(project)
    name = name or os.path.basename(project)
    postfix = postfix or git_rev(project) or ''
    wsgi_app = wsgi_app or f'{name}.wsgi:application'

    vars = {
        'project_name': name,
        'stage': stage,
        'project_src': project,
        'gunicorn_conf': gunicorn_conf,
        'wsgi_app': wsgi_app,
        'postfix': postfix,
    }

    if dry_run:
        print(vars)
        sys.exit(0)

    if debug:
        print(vars)

    owd = os.getcwd()
    wd = f'deployee-{uuid.uuid4()}'

    shutil.copytree('ansible', wd)
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
