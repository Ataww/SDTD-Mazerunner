#!/usr/bin/env python3

import os
import logging
import subprocess
import configparser
import socket

port_master = '7070'


# Function for launch Spark
def launch_spark():

    if isMaster():
        launch_server_zookeeper()
        launch_master()
    else:
        launch_slave()
    return


# Function for launch master
def launch_master():
    logging.info("Starting Spark Master ...")
    with open(os.path.expanduser('/home/xnet/spark/conf/spark-env.sh'), 'a') as confFile:
        subprocess.run(['echo', 'export SPARK_MASTER_HOST="' + get_hostname() + '"'], stdout=confFile, check=True)
    subprocess.run(['start-master'])
    return


# Function for launch slave
def launch_slave():
    logging.info("Starting Spark Worker ...")
    subprocess.run(['start-slave', 'spark://'+get_Master()+':'+port_master])
    return


# Function tu launch server zookeeper
def launch_server_zookeeper():
    logging.info("Starting Server Zookeeper ...")
    ZOOKEEPER_STATUS = os.popen('zkServer.sh start 2>&1 ', "r").read()
    if 'STARTED' in ZOOKEEPER_STATUS or 'already running' in ZOOKEEPER_STATUS:
        logging.info(" Zookeeper launched [success]")
    else:
        logging.error(" Zookeeper launch failed [error]")
    return


# Function for recover the address of master
def get_Master():
    master = "127.0.0.1"
    config = configparser.ConfigParser()
    config.read("./spark/conf.ini")
    hosts = getHostsByKey(config, "Master")
    for host in hosts:
        master = host
        return master
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

# Permit to know the hostname
def get_hostname():
    config = configparser.ConfigParser()
    config.read("./spark/conf.ini")
    hosts = getHostsByKey(config, "Master")
    hostname = socket.gethostname()

    for host in hosts:
        if host in hostname:
            return host

    hosts = getHostsByKey(config, "Slaves")
    for host in hosts:
        if host in hostname:
            return host

    return hostname

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
    launch_spark()