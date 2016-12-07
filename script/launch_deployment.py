#!/usr/bin/env python3

import configparser
import logging
import subprocess

components = ['hdfs','rabbitmq','spark']
#components = ['hdfs', 'neo4j', 'rabbitmq', 'spark']


# Function for copy the different script on the different machine
def install_environment():
    print("#############################################################")
    print("####### Installation of environment of all machines #########")
    print("#############################################################")
    # Read configuration
    logging.info("Read global configuration")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    for component in components:
        hosts = getHostsByKey(config,component)
        for host in hosts:
            logging.info("Set environment for component " + component + " on the machine with address " + host)
            logging.info('Start to get all files ... ')
            subprocess.run(['scp','-pq','-i','~/.ssh/xnet','./conf.ini','xnet@' + host + ':~'])
            subprocess.run(['scp','-pq','-i','~/.ssh/xnet','./install_config_machine.py','xnet@' + host + ':~'])
            subprocess.run(['ssh', '-i', '~/.ssh/xnet', 'xnet@' + host, 'rm -rf ' + component])
            out = subprocess.run(['scp', '-prq', '-i', '~/.ssh/xnet', './'+component,'xnet@' + host + ':~/'],check=True)
            if out.returncode == 0:
                logging.info("Transfer done [success]")
            else:
                logging.error("Transferring files failed [error]")
            subprocess.run(['ssh', '-i', '~/.ssh/xnet', 'xnet@' + host,'source ~/.profile; ./install_config_machine.py'])
            subprocess.run(['ssh', '-i', '~/.ssh/xnet', 'xnet@' + host,'source ~/.profile; ./'+component+'/install_'+component+'.py'])
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
    install_environment()