#!/usr/bin/env python3

import configparser
import socket
from .. import lib

port_master = '7070'


# Permit to know if it is zookeeper
def isZookeeper():
    config = configparser.ConfigParser()
    config.read("./spark/conf.ini")
    hosts = lib.getHostsByKey(config, "Zookeeper")
    hostname = socket.gethostname()

    for host in hosts:
        if host in hostname:
            return True
    return False


# Permit to know if it is master
def isMaster():
    config = configparser.ConfigParser()
    config.read("./spark/conf.ini")
    hosts = lib.getHostsByKey(config, "Master")
    hostname = socket.gethostname()

    for host in hosts:
        if host in hostname:
            return True
    return False


# Function for recover the address of master
def getSparkMaster():
    master = ''
    first = True
    config = configparser.ConfigParser()
    config.read("./spark/conf.ini")
    hosts = lib.getHostsByKey(config, "Master")
    for host in hosts:
        if first:
            master = host + ':' + port_master
            first = False
        else:
            master = master + ',' + host + ':' + port_master
    return master


# Permit to know the hostname
def get_hostname():
    config = configparser.ConfigParser()
    config.read("./spark/conf.ini")
    hosts = lib.getHostsByKey(config, "Master")
    hostname = socket.gethostname()

    for host in hosts:
        if host in hostname:
            return host

    hosts = lib.getHostsByKey(config, "Slaves")
    for host in hosts:
        if host in hostname:
            return host

    return hostname
