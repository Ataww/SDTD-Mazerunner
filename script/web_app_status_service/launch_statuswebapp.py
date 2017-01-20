#!/usr/bin/env python3

import logging
from subprocess import run
from logging import info


def launch():
    info('Starting Mazerunner WebApp Status')
    run(['sudo', 'systemctl', 'start', 'webapp_status'], check=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")
    launch()
