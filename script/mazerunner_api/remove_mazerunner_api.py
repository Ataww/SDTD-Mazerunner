#!/usr/bin/env python3

from subprocess import run
from logging import info

home = '/home/xnet'
mazerunner_api_script = home + "SDTD-Mazerunner/mazerunner/mazerunner_api.py"
mazerunner_api_service = home + "SDTD-Mazerunner/mazerunner/mazerunner_api.service"
mazerunner_api_dir = home + '/mazerunner_api' # contains the api script
systemd_dir = "/etc/systemd/system/"

def remove():
    info('Creating mazerunner_api folder')

    info('Disabling mazerunner_api service')
    run(['sudo', 'systemctl', 'disable', 'mazerunner_api'], check=True)

    info('Removing mazerunner_api.service')
    run(['sudo', 'rm', '-r', systemd_dir+"mazerunner_api.service"], check=True)


    run(['rm', '-rf', mazerunner_api_dir], check=True)

if __name__ == '__main__':
    remove()
