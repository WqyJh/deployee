# deployee

[![Build Status](https://travis-ci.org/WqyJh/deployee.svg?branch=master)](https://travis-ci.org/WqyJh/deployee)
[![license](https://img.shields.io/badge/LICENCE-GPLv3-brightgreen.svg)](https://raw.githubusercontent.com/WqyJh/deployee/master/LICENSE)

Server requirements:

- rsync
- supervisor
- python3
- virtualenv
- pip


## Usage

Deploy an django application.

```bash
deployee /path/to/project production
```

Deploy a flask application.

```bash
./run.py /path/to/project production --framework flask --script "python -m app"
```

## Project Structure

```bash
/var
├── lib
│   ├── local_settings
│   │   └── project
│   │       ├── production
│   │       ├── staging
│   │       └── test
│   └── venv
│   │   └── project
│   │       ├── production
|   |       |   └── <hash>
│   │       ├── staging
|   |       |   └── <hash>
│   │       └── test
├── log
│   └── project
│       ├── production
│       ├── staging
│       └── test
├── media
│   └── project
│       ├── production
│       ├── staging
│       └── test
├── static
│   └── project
│       ├── production
│       ├── staging
│       └── test
└── www
│   └── project
│       ├── production
|       |   └── <hash>
│       ├── staging
|       |   └── <hash>
│       └── test
```