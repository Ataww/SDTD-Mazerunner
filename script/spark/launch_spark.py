#!/usr/bin/env python3

import os
import logging
import subprocess
import configparser
import socket

port_master = '7070'
CODE_STARTING = 0
CODE_ALREADY_RUN = 256


# Function for launch Spark
def launch_spark():


    if isZookeeper():
        launch_server_zookeeper()
    if isMaster():
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
    out = os.system('start-slave spark://' + getSparkMaster() + ' >> /dev/null 2>&1')

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


# Function for recover the address of master
def getSparkMaster():
    master = ''
    first = True
    config = configparser.ConfigParser()
    config.read("./spark/conf.ini")
    hosts = getHostsByKey(config, "Master")
    for host in hosts:
        if first:
            master = host + ':' + port_master
            first = False
        else:
            master = master + ',' + host + ':' + port_master
    return master


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

# Permit to know if it is zookeeper
def isZookeeper():
    config = configparser.ConfigParser()
    config.read("./spark/conf.ini")
    hosts = getHostsByKey(config, "Zookeeper")
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
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    launch_spark()