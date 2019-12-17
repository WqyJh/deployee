# deployee

Server requirements:

- rsync
- supervisor
- python3
- virtualenv
- pip


## Usage

Deploy an django application.

```bash
./run.py /path/to/project production
```

Deploy a flask application.

```bash
./run.py /path/to/project production --framework flask --script python -m app
```
