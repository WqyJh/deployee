import os
import subprocess


def main():
    os.chdir('./ansible')
    subprocess.call(['ansible-playbook', 'playbook.yml'])


if __name__ == '__main__':
    main()
