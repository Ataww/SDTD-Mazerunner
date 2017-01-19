#!/usr/bin/env python3

import logging
from subprocess import run
from logging import info

home = '/home/xnet'
mazerunner_api_script = home + "SDTD-Mazerunner/mazerunner/mazerunner_api.py"
mazerunner_api_dir = home + '/mazerunner_api' # contains the api script


def stop():
    info('Stopping Mazerunner API')
    run(['rm -f /home/xnet/.neo4j/known_hosts'])
    run(['sudo', 'systemctl', 'stop', 'mazerunner_api'], check=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")
    stop()