#!/usr/bin/env python3

import configparser
import logging
import os
import socket
import subprocess

zookeeper_version = 'zookeeper-3.4.9'


# Function for install Zookeeper and its environment
def install_zookeeper():
    ZOOKEEPER_STATUS = os.popen('zkServer.sh status 2>&1 ', "r").read()
    if 'not found' in ZOOKEEPER_STATUS:
        logging.info("Downloading Zookeeper ...")
        out = subprocess.run(['wget', '-q',
                              'http://www-eu.apache.org/dist/zookeeper/' + zookeeper_version + '/' + zookeeper_version + '.tar.gz'],
                             check=True)
        if out.returncode == 0:
            logging.info("Downloading Zookeeper with [success]")
        else:
            logging.error("Failed to download Zookeeper [error]")
        logging.info("Installation of Zookeeper ...")
        subprocess.run(['sudo', 'rm', '-rf', '/usr/lib/zookeeper'])
        subprocess.run(['sudo', 'mkdir', '/usr/lib/zookeeper'])
        out = subprocess.run(['sudo', 'tar', '-xf', 'zookeeper-3.4.9.tar.gz', '-C', '/usr/lib/zookeeper'], check=True)
        if out.returncode == 0:
            logging.info("Zookeeper unpacked [success]")
        else:
            logging.error("Failed to unpack Zookeeper [error]")
        subprocess.run(['rm', zookeeper_version + '.tar.gz'])
        os.system(
            'echo export PATH=$PATH:/usr/lib/zookeeper/' + zookeeper_version + '/bin | sudo tee -a /etc/environment >> /dev/null 2>&1')
        logging.info("Zookeeper configuration")
        set_server_value_zookeeper()
        define_id_zookeeper()
        # ZOOKEEPER_STATUS = os.popen('zkServer.sh status 2>&1 ', "r").read()
        # if 'not found' in ZOOKEEPER_STATUS:
        #    logging.info(" Zookeeper is installed with [success]")
        # else:
        #    logging.error(" Zookeeper couldn't be install [error]")
    return


# Permit to define the server value for the file zoo.cfg
def set_server_value_zookeeper():
    index = 1
    port_com_leader = 2888
    port_elec_leader = 3888
    config = configparser.ConfigParser()
    config.read("conf.ini")
    hosts = getHostsByKey(config, "Zookeeper")

    subprocess.run(['sudo', 'cp', '/home/xnet/SDTD-Mazerunner/script/zookeeper/conf/zoo.cfg',
                    '/usr/lib/zookeeper/' + zookeeper_version + '/conf/zoo.cfg'])

    for host in hosts:
        os.system('echo server.' + str(index) + '=' + host + ':' + str(port_com_leader) + ':' + str(
            port_elec_leader) + ' | sudo tee -a /usr/lib/zookeeper/' + zookeeper_version + '/conf/zoo.cfg >> /dev/null 2>&1')

        index += 1
    return


def define_id_zookeeper():
    id = 1
    config = configparser.ConfigParser()
    config.read("conf.ini")
    hosts = getHostsByKey(config, "Zookeeper")
    hostname = socket.gethostname()
    subprocess.run(['mkdir', '/usr/lib/zookeeper/' + zookeeper_version + '/tmp/'])
    for host in hosts:
        if host in hostname:
            with open(os.path.expanduser('/usr/lib/zookeeper/' + zookeeper_version + '/tmp/myid'), 'a') as idFile:
                subprocess.run(['echo', str(id)], stdout=idFile, check=True)
            return
        id += 1
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
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

    install_zookeeper()
