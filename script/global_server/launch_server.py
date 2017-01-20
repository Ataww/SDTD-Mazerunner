#!/usr/bin/env python3

import logging
from subprocess import run
from logging import info


def launch():
    info('Starting Mazerunner Server Status')
    run(['sudo', 'systemctl', 'start', 'scheduler_server'], check=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")
    launch()
