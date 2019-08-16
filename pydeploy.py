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
from format import format as _




class Config(object):
    def __init__(self, name=''):
        self.cwd = os.getcwd()
        basename = os.path.basename(self.cwd)
        name = name if name else basename

        production_name = name
        staging_name = _('{name}-staging')
        test_name = _('{name}-test')
        
        user = 'www-data'
        group = 'www-data'

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

        gitrev = git['rev-parse', '--short', 'HEAD']
        dest = _('{prefix}/{name}')
        logging_path = _('{logging_prefix}/{name}')
        media_path = _('{media_prefix}/{name}')
        static_path = _('{static_prefix}/{name}')

        venv_name = _('{name}-{gitrev}')
        venv_path = _('{venv_prefix}/{venv_name}')
        venv_python = _('{venv_path}/bin/python')
        venv_gunicorn = _('{venv_path}/bin/gunicorn')

        local_settings_path = _('{local_settings_prefix}/{name}')
        
            

