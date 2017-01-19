#!/usr/bin/env python3

import os
import logging
from lib_spark import isMaster

CODE_STOP = 0


# Function for launch Spark
def stop_environement_spark():
    if isMaster():
        stop_master()
    else:
        stop_slave()
    return


# Function for stop master
def stop_master():
    logging.info("Stopping Spark Master ...")
    out = os.system('stop-master >> /dev/null 2>&1')
    if out == CODE_STOP:
        logging.info("Spark master is stop [success]")
    else:
        logging.error("Spark master stop failed [error]")
    return


# Function for stop slave
def stop_slave():
    logging.info("Stopping Spark Worker ...")
    out = os.system('stop-slave >> /dev/null 2>&1')
    if out == CODE_STOP:
        logging.info("Spark slave is stop [success]")
    else:
        logging.error("Spark slave stop failed [error]")
    return


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

    stop_environement_spark()
