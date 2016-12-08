#!/usr/bin/env python3

import os
import logging
import subprocess
import configparser
import socket

CODE_STOP = 0

# Function for launch Spark
def stop_spark():

    if isMaster():
        stop_server_zookeeper()
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


# Function tu stop server zookeeper
def stop_server_zookeeper():
    logging.info("stop Server Zookeeper ...")
    ZOOKEEPER_STATUS = os.popen('zkServer.sh stop 2>&1 ', "r").read()
    if 'STOPPED' in ZOOKEEPER_STATUS:
        logging.info(" Zookeeper stopped [success]")
    elif 'no zookeeper to stop' in ZOOKEEPER_STATUS:
        logging.info(" Zookeeper is already stop [success]")
    else:
        logging.error(" Zookeeper stopped failed [error]")
    return

# Permit to know if it is master
def isMaster():
    config = configparser.ConfigParser()
    config.read("./spark/conf.ini")
    hosts = getHostsByKey(config, "Master")
    hostname = socket.gethostname()

    for host in hosts:
        if host in hostname:
            return True
    return False

# Recover all ip for one component. Return format ip
def getHostsByKey(config, key):
    hosts = config.get(key, "hosts").split(',')
    index = 0
    for host in hosts:
        hosts[index] = host.strip(' \n')
        index += 1
    return hosts

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    stop_spark()