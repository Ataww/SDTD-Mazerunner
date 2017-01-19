#!/usr/bin/env python3

import logging

from subprocess import run
from logging import info
from os.path import exists

home = '/home/xnet'
mazerunner_api_script = home + "SDTD-Mazerunner/mazerunner/mazerunner_api.py"
mazerunner_api_service = home + "SDTD-Mazerunner/mazerunner/mazerunner_api.service"
mazerunner_api_dir = home + '/mazerunner_api' # contains the api script
systemd_dir = "/etc/systemd/system/"


def install_mazerunner_api():
    """Install mazerunner_api """
    if not exists(mazerunner_api_dir):
        info('Creating mazerunner_api folder')
        run(['mkdir', mazerunner_api_dir], check=True)

        info('Copying mazerunner_api script into its installation folder')
        run(['cp', mazerunner_api_script, mazerunner_api_dir], check=True)

        info('Copying mazerunner_api.service file to /etc/systemd/system/')
        run(['cp', mazerunner_api_service, systemd_dir], check=True)

        info('Installing pywebhdfs python module')
        run(['sudo', '-H', 'pip3', 'install', 'pywebhdfs'], check=True)

        info('Installing pywebhdfs neo4j-driver module')
        run(['sudo', '-H', 'pip3', 'install', 'neo4j-driver'], check=True)

        info('Installing flask python module')
        run(['sudo', '-H', 'pip3', 'install', 'flask'], check=True)

        info('Installing pika python module')
        run(['sudo', '-H', 'pip3', 'install', 'pika'], check=True)

        info('Activating mazerunner_api service')
        run(['sudo', 'systemctl', 'enable', 'mazerunner_api'], check=True)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO ,format="%(asctime)s :: %(levelname)s :: %(message)s")
    install_mazerunner_api()
