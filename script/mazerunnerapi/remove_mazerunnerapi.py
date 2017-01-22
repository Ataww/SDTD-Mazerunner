#!/usr/bin/env python3

from subprocess import run
from logging import info

home = '/home/xnet'
mazerunner_api_script = home + "SDTD-Mazerunner/mazerunner/mazerunnerapi.py"
mazerunner_api_service = home + "SDTD-Mazerunner/mazerunner/scheduler_server.service"
mazerunner_api_dir = home + '/mazerunnerapi' # contains the api script
systemd_dir = "/etc/systemd/system/"

def remove():
    info('Creating mazerunnerapi folder')

    info('Disabling mazerunnerapi service')
    run(['sudo', 'systemctl', 'disable', 'mazerunnerapi'], check=True)

    info('Removing scheduler_server.service')
    run(['sudo', 'rm', '-r', systemd_dir+"scheduler_server.service"], check=True)


    run(['rm', '-rf', mazerunner_api_dir], check=True)

if __name__ == '__main__':
    remove()
