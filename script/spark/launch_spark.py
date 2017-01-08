#!/usr/bin/env python3

import os
import logging
from . import lib_spark

CODE_STARTING = 0
CODE_ALREADY_RUN = 256


# Function for launch Spark
def launch_spark():
    if lib_spark.isZookeeper():
        launch_server_zookeeper()
    if lib_spark.isMaster():
        launch_master()
    else:
        launch_slave()
    return


# Function for launch master
def launch_master():
    logging.info("Starting Spark Master ...")
    out = os.system('start-master >> /dev/null 2>&1')
    if out == CODE_STARTING:
        logging.info("Spark master are launched [success]")
    elif out == CODE_ALREADY_RUN:
        logging.info("Spark master is already launched [success]")
    else:
        logging.error("Spark master launch failed [error]")
    return


# Function for launch slave
def launch_slave():
    logging.info("Starting Spark Worker ...")
    out = os.system('start-slave spark://' + lib_spark.getSparkMaster() + ' >> /dev/null 2>&1')

    if out == CODE_STARTING:
        logging.info("Spark slaves are launched [success]")
    elif out == CODE_ALREADY_RUN:
        logging.info("Spark slaves is already launched [success]")
    else:
        logging.error("Spark slaves launch failed [error]")
    return


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
    launch_spark()
