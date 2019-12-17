import os
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
def main(project, stage, name=None, gunicorn_conf=None, wsgi_app=None, postfix=None):
    project = os.path.abspath(project)
    name = name or os.path.basename(project)
    postfix = postfix or git_rev(project) or ''
    wsgi_app = wsgi_app or f'{name}.wsgi:application'

    owd = os.getcwd()
    wd = f'deployee-{uuid.uuid4()}'

    shutil.copytree('ansible', wd)
    os.chdir(wd)

    vars = {
        'project_name': name,
        'stage': stage,
        'project_src': project,
        'gunicorn_conf': gunicorn_conf,
        'wsgi_app': wsgi_app,
        'postfix': postfix,
    }

    print(vars)

    with open('vars.yml', 'w') as f:
        f.write(yaml.dump(vars))

    subprocess.call(['ansible-playbook', 'playbook.yml'])

    os.chdir(owd)
    shutil.rmtree(wd)


if __name__ == '__main__':
    main()
