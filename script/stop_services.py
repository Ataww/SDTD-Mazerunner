#!/usr/bin/env python3

import configparser
import logging
import subprocess

components = ['hdfs','rabbitmq','spark']
#components = ['hdfs', 'neo4j', 'rabbitmq', 'spark']

# Function who will stop the different component
def stop_component():
    print("############################################################")
    print("###### Stop the different components on machines ###########")
    print("############################################################")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    for component in components:
        hosts = getHostsByKey(config, component)
        for host in hosts:
            logging.info("Stop component " + component + " on the machine with address " + host)
            subprocess.run(['ssh','-o','StrictHostKeyChecking=no','-i','~/.ssh/xnet','xnet@'+host,'source ~/.profile; ./'+component+'/stop_'+component+'.py'])
    return

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
    stop_component()