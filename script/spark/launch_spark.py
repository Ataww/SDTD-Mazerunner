#!/usr/bin/env python3

import os
import logging
import subprocess

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
    logging.info(" Starting Spark Master ...")
    with open(os.path.expanduser('/home/xnet/spark/conf/spark-env.sh'), 'a') as confFile:
        subprocess.run(['echo', 'export SPARK_MASTER_HOST="' + get_ip() + '"'], stdout=confFile, check=True)
    subprocess.run(['stop-master'])
    subprocess.run(['start-master'])
    return


# Function for launch slave
def launch_slave():
    logging.info(" Starting Spark Worker ...")
    subprocess.run(['stop-slave'])
    subprocess.run(['start-slave', 'spark://'+get_Ip_Master()+':'+port_master])
    return


# Function tu launch server zookeeper
def launch_server_zookeeper():
    logging.info(" Starting Server Zookeeper ...")
    ZOOKEEPER_STATUS = os.popen('zkServer.sh start 2>&1 ', "r").read()
    if 'STARTED' in ZOOKEEPER_STATUS:
        logging.info(" Zookeeper launched [success]")
    else:
        logging.error(" Zookeeper launch failed [error]")
    return


# Function for recover the address of master
def get_Ip_Master():
    file = open('./spark/master.txt')
    ip_master = "127.0.0.1"
    for host in file:
        ip_master = host.strip(' \n')
        return ip_master
    return ip_master


# Permit to know if it is master
def isMaster():
    result = False
    ip = get_ip()
    file = open('./spark/master.txt')
    for host in file:
        if ip in host:
            result = True
    file.close()
    return result


# Get the ip of the current machine
def get_ip():
    ip = os.popen('ifconfig ens3 | grep "inet ad" | cut -f2 -d: | awk \'{print $1}\'', "r").read()
    ip = ip.strip(' \n')
    return ip

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    launch_spark()