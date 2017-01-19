#!/usr/bin/env python3

import os
import logging


# Function tu stop server zookeeper
def stop_server_zookeeper():
    logging.info("stop Server Zookeeper ...")
    ZOOKEEPER_STATUS = os.popen('zkServer.sh stop 2>&1 ', "r").read()
    if 'STOPPED' in ZOOKEEPER_STATUS:
        logging.info("Zookeeper stopped [success]")
    elif 'no zookeeper to stop' in ZOOKEEPER_STATUS:
        logging.info("Zookeeper is already stop [success]")
    else:
        logging.error("Zookeeper stopped failed [error]")
    return


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

    stop_server_zookeeper()
