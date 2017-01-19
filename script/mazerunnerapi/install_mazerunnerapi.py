#!/usr/bin/env python3

import logging

from subprocess import run
from logging import info
from os.path import exists

home = '/home/xnet'
mazerunner_api_script = home + "/SDTD-Mazerunner/mazerunner/mazerunnerapi.py"
mazerunner_api_service = home + "/SDTD-Mazerunner/mazerunner/mazerunnerapi.service"
mazerunner_api_dir = home + '/mazerunnerapi' # contains the api script
systemd_dir = "/etc/systemd/system/"


def install_mazerunner_api():
    """Install mazerunnerapi """
    if not exists(mazerunner_api_dir):
        info('Creating mazerunnerapi folder')
        run(['mkdir', mazerunner_api_dir], check=True)

        info('Copying mazerunnerapi script into its installation folder')
        run(['cp', mazerunner_api_script, mazerunner_api_dir], check=True)

        info('Copying mazerunnerapi.service file to /etc/systemd/system/')
        run(['sudo', 'rm', systemd_dir+'mazerunnerapi.service'])
        run(['sudo', 'cp', mazerunner_api_service, systemd_dir], check=True)

        info('Installing pywebhdfs python module')
        run(['sudo', '-H', 'pip3', 'install', 'pywebhdfs'], check=True)

        info('Installing pywebhdfs neo4j-driver module')
        run(['sudo', '-H', 'pip3', 'install', 'neo4j-driver'], check=True)

        info('Installing flask python module')
        run(['sudo', '-H', 'pip3', 'install', 'flask'], check=True)

        info('Installing pika python module')
        run(['sudo', '-H', 'pip3', 'install', 'pika'], check=True)

        info('Activating mazerunnerapi service')
        run(['sudo', 'systemctl', 'enable', 'mazerunnerapi'], check=True)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO ,format="%(asctime)s :: %(levelname)s :: %(message)s")
    install_mazerunner_api()
