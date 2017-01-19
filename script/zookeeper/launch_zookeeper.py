#!/usr/bin/env python3

import os
import logging


# Function tu launch server zookeeper
def launch_server_zookeeper():
    logging.info("Starting Server Zookeeper ...")
    ZOOKEEPER_STATUS = os.popen('zkServer.sh start 2>&1 ', "r").read()
    if 'STARTED' in ZOOKEEPER_STATUS:
        logging.info("Zookeeper launched [success]")
    elif 'already running' in ZOOKEEPER_STATUS:
        logging.info("Zookeeper is already running [success]")
    else:
        logging.error("Zookeeper launch failed [error]")
    return


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

    launch_server_zookeeper()
