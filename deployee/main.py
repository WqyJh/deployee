import os
import uuid
import yaml
import shutil
import subprocess


def git_rev(repo):
    ret = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], cwd=repo)
    ret = ret.decode().strip()
    return ret


def main():
    owd = os.getcwd()
    wd = f'tmp-{uuid.uuid4()}'

    shutil.copytree('ansible', wd)
    os.chdir(wd)

    vars = {
        'project_name': 'dian_recruit',
        'stage': 'staging',
        'project_src': '/home/linux/Works/VSCodeProject/dian_recruit/Dian',
        'supervisord_conf': '/etc/supervisord.conf',
        'supervisor_prefix': '/etc/supervisord.d',
        'supervisor_ext': 'ini',
        'gunicorn_conf': 'gunicorn.conf.py',
        'wsgi_app': 'Dian.wsgi:application',
        'postfix': 'f606bc8',
    }

    vars['postfix'] = git_rev(vars['project_src'])

    with open('vars.yml', 'w') as f:
        f.write(yaml.dump(vars))

    subprocess.call(['ansible-playbook', 'playbook.yml'])


    os.chdir(owd)
    shutil.rmtree(wd)


if __name__ == '__main__':
    main()
