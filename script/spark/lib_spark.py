#!/usr/bin/env python3

import configparser
import socket

port_master = '7070'


# Permit to know if it is zookeeper
def isZookeeper():
    config = configparser.ConfigParser()
    config.read("conf.ini")
    hosts = getHostsByKey(config, "Zookeeper")
    hostname = socket.gethostname()

    for host in hosts:
        if host in hostname:
            return True
    return False


# Permit to know if it is master
def isMaster():
    config = configparser.ConfigParser()
    config.read("conf.ini")
    hosts = getHostsByKey(config, "Master")
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
    config.read("conf.ini")
    hosts = getHostsByKey(config, "Master")
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
    config.read("conf.ini")
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
