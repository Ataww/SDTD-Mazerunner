#!/usr/bin/env python3

import configparser
import logging
import subprocess
import os

components = ['hdfs', 'neo4j', 'rabbitmq', 'spark']


# Function who will launch the different component
def launch_component():
    print("############################################################")
    print("###### Launch the different components on machines #########")
    print("############################################################")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    for component in components:
        hosts = getHostsByKey(config, component)
        for host in hosts:
            if hostIsUp(host):
                logging.info("Launch component " + component + " on the machine with address " + host)
                subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + host,
                                'source ~/.profile; cd SDTD-Mazerunner/script/'+component+'/; python3 launch_' + component + '.py'])
            else:
                logging.error("Impossible d'accéder à la machine " + host)
    return


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
            if hostIsUp(host):
                logging.info("Stop component " + component + " on the machine with address " + host)
                subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + host,
                                'source ~/.profile; cd SDTD-Mazerunner/script/'+component+'/; python3 stop_' + component + '.py'])
            else:
                logging.error("Impossible d'accéder à la machine " + host)
    return

# Function for update fill on all Machine
def update_all_server():
    print("############################################################")
    print("############# Update the different  machines ###############")
    print("############################################################")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    for component in components:
        hosts = getHostsByKey(config, component)
        for host in hosts:
            if hostIsUp(host):
                logging.info("Update component " + component + " on the machine with address " + host)
                updateFileServer(host)
            else:
                logging.error("Impossible d'accéder à la machine " + host)
    return

# Function for remove all service on all Machine
def remove_all_server():
    print("############################################################")
    print("######## Remove the different service on machines ##########")
    print("############################################################")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    for component in components:
        hosts = getHostsByKey(config, component)
        for host in hosts:
            if hostIsUp(host):
                logging.info("Remove component " + component + " on the machine with address " + host)
                subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + host,
                                'source ~/.profile; cd SDTD-Mazerunner/script/'+component+'/; python3 remove_' + component + '.py'])
            else:
                logging.error("Impossible d'accéder à la machine " + host)
    return

# Function for install all service on all Machine
def install_all_server():
    print("############################################################")
    print("######## install the different service on machines ##########")
    print("############################################################")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    for component in components:
        hosts = getHostsByKey(config, component)
        for host in hosts:
            if hostIsUp(host):
                logging.info("Install component " + component + " on the machine with address " + host)
                subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + host,
                                'source ~/.profile; cd SDTD-Mazerunner/script/'+component+'/; python3 install_' + component + '.py'])
            else:
                logging.error("Impossible d'accéder à la machine " + host)
    return

# Function for install basic config on all Machine
def install_basic_config():
    print("############################################################")
    print("###### install the basic config service on machines ########")
    print("############################################################")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    for component in components:
        hosts = getHostsByKey(config, component)
        for host in hosts:
            if hostIsUp(host):
                logging.info("Install basic config on the machine with address " + host)
                subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + host,
                                'source ~/.profile; cd SDTD-Mazerunner/script/; python3 install_config_machine.py'])
            else:
                logging.error("Impossible d'accéder à la machine " + host)
    return



# Recover all ip for one component. Return format ip
def getHostsByKey(config, key):
    hosts = config.get(key, "hosts").split(',')
    index = 0
    for host in hosts:
        hosts[index] = host.strip(' \n')
        index += 1
    return hosts

# Function for check host
def hostIsUp(host):
    if os.system('ping -c 1 ' + host + ' >> /dev/null 2>&1'):
        return False
    return True

# Function for update file on specific server
def updateFileServer(ip):
    out = subprocess.run(['tar', 'czf', '/tmp/SDTD-Mazerunner-Script.tar.gz', '.'],
                         cwd=os.getcwd(),
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if out.returncode == 0:
        logging.info("Compressing directory done [success]")
    else:
        logging.error("Compressing directory failed [error]")
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + ip,
                          'rm -rf SDTD-Mazerunner/script/'])
    out = subprocess.run(
        ['scp', '-pq', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', '/tmp/SDTD-Mazerunner-Script.tar.gz',
         'xnet@' + ip + ':~/'], check=True)
    if out.returncode == 0:
        logging.info("Transfer done [success]")
    else:
        logging.error("Transferring files failed [error]")
    logging.info("Detar file ...")
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + ip,
                          'mkdir -p SDTD-Mazerunner/script'])
    out = subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + ip,
                          'tar xzf SDTD-Mazerunner-Script.tar.gz -C SDTD-Mazerunner/script'])
    if out.returncode == 0:
        logging.info("Decompressing directory done [success]")
    else:
        logging.error("Decompressing directory failed [error]")
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + ip,
                          'rm SDTD-Mazerunner-Script.tar.gz'])
    return
