#!/usr/bin/env python3

import configparser
import logging
import subprocess
import os

components = ['hdfs', 'neo4j', 'rabbitmq', 'spark', 'zookeeper', 'mazerunnerapi', 'webapp']


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
                                'source ~/.profile; cd SDTD-Mazerunner/script/' + component + '/; python3 launch_' + component + '.py'])
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
                                'source ~/.profile; cd SDTD-Mazerunner/script/' + component + '/; python3 stop_' + component + '.py'])
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
                                'source ~/.profile; cd SDTD-Mazerunner/script/' + component + '/; python3 remove_' + component + '.py'])
            else:
                logging.error("Impossible d'accéder à la machine " + host)
    return


# Function for install all service on all Machine
def install_all_server():
    print("#############################################################")
    print("######## install the different service on machines ##########")
    print("#############################################################")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    for component in components:
        hosts = getHostsByKey(config, component)
        for host in hosts:
            if hostIsUp(host):
                logging.info("Install component " + component + " on the machine with address " + host)
                subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + host,
                                'source ~/.profile; cd SDTD-Mazerunner/script/' + component + '/; python3 install_' + component + '.py'])
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


# Install Cluster
def install_cluster(service_name):
    print("############################################################")
    print("######               install cluster                ########")
    print("############################################################")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    hosts = getHostsByKey(config, service_name)
    for host in hosts:
        if hostIsUp(host):
            logging.info("Install service " + service_name + " on the machine with address " + host)
            subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + host,
                            'source ~/.profile; cd SDTD-Mazerunner/script/' + service_name + '/; python3 install_' + service_name + '.py'])
        else:
            logging.error("Impossible d'accéder à la machine " + host)
    return


# Launch Cluster
def launch_cluster(service_name):
    print("############################################################")
    print("######               launch cluster                #########")
    print("############################################################")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    hosts = getHostsByKey(config, service_name)
    for host in hosts:
        if hostIsUp(host):
            logging.info("Launch service " + service_name + " on the machine with address " + host)
            subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + host,
                            'source ~/.profile; cd SDTD-Mazerunner/script/' + service_name + '/; python3 launch_' + service_name + '.py'])
        else:
            logging.error("Impossible d'accéder à la machine " + host)
    return


# Permit to stop web app
def stop_web_app(port, ip):
    cond = True
    while cond:
        p = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                              'xnet@' + ip,
                              'source ~/.profile; netstat -pa | grep ' + str(
                                  port) + ' | grep \'python3\' | grep \'LISTEN\' | awk \'{print $7}\''],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        out = p.stdout.read().decode("utf-8")
        if 'python3' in out:
            pid = out.replace('/python3', '').strip(' \n')
            subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + ip,
                            'source ~/.profile; kill -9 ' + pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            cond = False
    return


# Permit to know if web app is launch
def web_app_status(port, ip):
    p = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                          'xnet@' + ip,
                          'source ~/.profile; netstat -pa | grep ' + str(
                              port) + ' | grep \'python3\' | grep \'LISTEN\' | awk \'{print $7}\''],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    out = p.stdout.read().decode("utf-8")
    if 'python3' in out:
        pid = out.replace('/python3', '').strip(' \n')
        subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + ip,
                        'source ~/.profile; kill -9 ' + pid], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    else:
        return False


def update_directory_mazerunner_api():
    print("############################################################")
    print("################# Update Mazerunner Api ####################")
    print("############################################################")
    config = configparser.ConfigParser()
    config.read("./mazerunnerapi/conf.ini")
    hosts = getHostsByKey(config, 'mazerunner_api_active')
    for host in hosts:
        if hostIsUp(host):
            logging.info("Update component Mazerunner-api on the machine with address " + host)
            updateFileServer(host)
            updateFileServerMazerunner(host)
        else:
            logging.error("Impossible d'accéder à la machine " + host)
    hosts = getHostsByKey(config, 'mazerunner_api_standby')
    for host in hosts:
        if hostIsUp(host):
            logging.info("Update component Mazerunner-api on the machine with address " + host)
            updateFileServer(host)
            updateFileServerMazerunner(host)
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


# Function for update file for api mazerunner
def updateFileServerMazerunner(ip):
    out = subprocess.run(['tar', 'czf', '/tmp/SDTD-Mazerunner-api.tar.gz', '.'],
                         cwd=os.getcwd().replace('/script', '/mazerunner'),
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    if out.returncode == 0:
        logging.info("Compressing directory done [success]")
    else:
        logging.error("Compressing directory failed [error]")
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + ip,
                    'sudo rm -rf SDTD-Mazerunner/mazerunner/'])
    out = subprocess.run(
        ['scp', '-pq', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', '/tmp/SDTD-Mazerunner-api.tar.gz',
         'xnet@' + ip + ':~/'], check=True)
    if out.returncode == 0:
        logging.info("Transfer done [success]")
    else:
        logging.error("Transferring files failed [error]")
    logging.info("Detar file ...")
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + ip,
                    'mkdir -p SDTD-Mazerunner/mazerunner'])
    out = subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + ip,
                          'tar xzf SDTD-Mazerunner-api.tar.gz -C SDTD-Mazerunner/mazerunner/'])
    if out.returncode == 0:
        logging.info("Decompressing directory done [success]")
    else:
        logging.error("Decompressing directory failed [error]")
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + ip,
                    'rm SDTD-Mazerunner-api.tar.gz'])
    return


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
                    'sudo rm -rf SDTD-Mazerunner/script/'])
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
