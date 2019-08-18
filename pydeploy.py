'''
Directories structure of deployment
/var
├── lib
│   ├── local_settings
│   │   ├── project
│   │   ├── project-staging
│   │   └── project-test
│   └── venv
│       ├── project
│       ├── project-staging
│       └── project-test
├── log
│   ├── project
│   └── project-staging
├── media
│   ├── project
│   └── project-staging
├── static
│   ├── project
│   └── project-staging
└── www
    ├── project
    └── project-staging
'''

import os
from plumbum.cmd import git
from plumbum.commands import TEE

from format import format as _


class Config(object):
    def __init__(self, name=''):
        self.cwd = os.getcwd()
        basename = os.path.basename(self.cwd)
        name = name if name else basename

        self.name = name

        self.user = 'www-data'
        self.group = 'www-data'

        prefix = '/var/www'
        logging_prefix = '/var/log'
        media_prefix = '/var/media'
        static_prefix = '/var/static'
        venv_prefix = '/var/lib/venv'
        local_settings_prefix = '/var/lib/local_settings'

        if os.path.isdir('/etc/supervisor'):
            supervisor_prefix = '/etc/supervisor/conf.d'
            supervisor_config = _('{supervisor_prefix}/{name}.conf')
        else:
            supervisor_prefix = '/etc/supervisord.d'
            supervisor_config = _('{supervisor_prefix}/{name}.ini')

        gitrev = (git['rev-parse', '--short', 'HEAD'] & TEE)[1].strip()
        dest = _('{prefix}/{name}')
        logging_path = _('{logging_prefix}/{name}')
        media_path = _('{media_prefix}/{name}')
        static_path = _('{static_prefix}/{name}')

        venv_name = _('{name}-{gitrev}')
        venv_path = _('{venv_prefix}/{venv_name}')
        venv_python = _('{venv_path}/bin/python')
        venv_gunicorn = _('{venv_path}/bin/gunicorn')

        local_settings_path = _('{local_settings_prefix}/{name}')

        self.dest = dest
        self.prefix = prefix
        self.supervisor_prefix = supervisor_prefix
        self.supervisor_config = supervisor_config
        self.logging_path = logging_path
        self.media_path = media_path
        self.static_path = static_path
        self.venv_path = venv_path
        self.venv_python = venv_python
        self.venv_gunicorn = venv_gunicorn
        self.local_settings_path = local_settings_path


def print_config(config):
    print('name:', config.name)
    print('user:', config.user)
    print('group:', config.group)
    print('prefix:', config.prefix)
    print('logging_path:', config.logging_path)
    print('media_path:', config.media_path)
    print('static_path:', config.static_path)
    print('ven_path:', config.venv_path)
    print('local_settings_path:', config.local_settings_path)
    print('supervisor_prefix:', config.supervisor_prefix)
    print('supervisor_config:', config.supervisor_config)
    print('dest:', config.dest)
    print('venv_path:', config.venv_path)
    print('venv_python:', config.venv_python)
    print('venv_gunicorn:', config.venv_gunicorn)
    print('local_settings_path', config.local_settings_path)


def print_full_config():
    def _wrap_title(title, config):
        print(_('[{title}] info'))
        print_config(config)
        print()

    production_config = Config(name='deployee')
    staging_config = Config(name='deployee-staging')
    test_config = Config(name='deployee-test')

    _wrap_title('production', production_config)
    _wrap_title('staging', staging_config)
    _wrap_title('test', test_config)

print_full_config()