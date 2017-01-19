#!/usr/bin/env python3

import logging
from subprocess import run
from logging import info
import subprocess

home = '/home/xnet'
mazerunner_api_script = home + "/SDTD-Mazerunner/mazerunner/mazerunnerapi.py"
mazerunner_api_dir = home + '/mazerunnerapi'  # contains the api script


def stop():
    info('Stopping Mazerunner API')
    run(['rm', '-f', '/home/xnet/.neo4j/known_hosts'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    run(['sudo', 'systemctl', 'stop', 'mazerunnerapi'], check=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")
    stop()
