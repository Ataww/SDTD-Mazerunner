#!/usr/bin/env python3

import os
import logging
import subprocess
import configparser
import socket

spark_version = 'spark-2.0.2-bin-without-hadoop'
zookeeper_version = 'zookeeper-3.4.9'
spark_home = 'SPARK_HOME=/usr/lib/spark/'+spark_version
spark_conf_dir = 'SPARK_CONF_DIR=/home/xnet/spark/conf'


# Function for install Spark and its environment
def install_spark():
    SPARK_STATUS = os.popen('stop-master 2>&1 ', "r").read()
    if 'not found' in SPARK_STATUS:
        logging.info("Downloading Spark ...")
        out = subprocess.run(['wget', '-q', 'http://d3kbcqa49mib13.cloudfront.net/'+spark_version+'.tgz'], check=True)
        if out.returncode == 0:
            logging.info("Spark downloaded [success]")
        logging.info("Installation of Spark ...")
        subprocess.run(['sudo', 'rm', '-rf', '/usr/lib/spark'])
        subprocess.run(['sudo', 'mkdir', '/usr/lib/spark'])
        out = subprocess.run(['sudo', 'tar', '-xf',spark_version+'.tgz', '-C', '/usr/lib/spark'], check=True)
        if out.returncode == 0:
            logging.info("Spark unpacked [success]")
        subprocess.run(['rm',spark_version+'.tgz'])
        subprocess.run(['sudo', 'ln', '-s', '/usr/lib/spark/'+spark_version+'/sbin/start-master.sh', '/sbin/start-master'])
        subprocess.run(['sudo', 'ln', '-s', '/usr/lib/spark/'+spark_version+'/sbin/stop-master.sh', '/sbin/stop-master'])
        subprocess.run(['sudo', 'ln', '-s', '/usr/lib/spark/'+spark_version+'/sbin/start-slave.sh', '/sbin/start-slave'])
        subprocess.run(['sudo', 'ln', '-s', '/usr/lib/spark/'+spark_version+'/sbin/stop-slave.sh', '/sbin/stop-slave'])
        if not isAlreadyAdd('/etc/environment', spark_home):
            os.system('echo ' + spark_home + ' | sudo tee -a /etc/environment >> /dev/null 2>&1')
        if not isAlreadyAdd('/etc/environment', spark_conf_dir):
            os.system('echo ' + spark_conf_dir + ' | sudo tee -a /etc/environment >> /dev/null 2>&1')
        subprocess.run(['sudo', 'mkdir', '/usr/lib/spark/'+spark_version+'/logs'])
        subprocess.run(['sudo', 'chmod', '777','-R', '/usr/lib/spark/'+spark_version+'/logs'])
        subprocess.run(['sudo', 'mkdir', '/usr/lib/spark/'+spark_version+'/work'])
        subprocess.run(['sudo', 'chmod', '777','-R', '/usr/lib/spark/'+spark_version+'/work'])
        SPARK_STATUS = os.popen('stop-master 2>&1 ', "r").read()
        if 'not found' not in SPARK_STATUS:
            logging.info("Spark installed [success]")
        else:
            logging.error("Spark installation failed [error]")
    return


# Function for install Zookeeper and its environment
def install_zookeeper():
    ZOOKEEPER_STATUS = os.popen('zkServer.sh status 2>&1 ', "r").read()
    if 'not found' in ZOOKEEPER_STATUS:
        logging.info("Downloading Zookeeper ...")
        out = subprocess.run(['wget', '-q', 'http://www-eu.apache.org/dist/zookeeper/'+zookeeper_version+'/'+zookeeper_version+'.tar.gz'], check=True)
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
        subprocess.run(['rm', zookeeper_version+'.tar.gz'])
        with open(os.path.expanduser('~/.profile'), 'a') as proFile:
            subprocess.run(['echo', 'export PATH=$PATH:/usr/lib/zookeeper/'+zookeeper_version+'/bin'], stdout=proFile, check=True)
        logging.info("Zookeeper configuration")
        set_server_value_zookeeper()
        define_id_zookeeper()
        subprocess.run(['sudo', 'cp', '/home/xnet/spark/conf/zoo.cfg', '/usr/lib/zookeeper/'+zookeeper_version+'/conf/zoo.cfg'])
        # ZOOKEEPER_STATUS = os.popen('zkServer.sh status 2>&1 ', "r").read()
        # if 'not found' in ZOOKEEPER_STATUS:
        #    logging.info(" Zookeeper is installed with [success]")
        # else:
        #    logging.error(" Zookeeper couldn't be install [error]")
    return


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

# Permit to define the server value for the file zoo.cfg
def set_server_value_zookeeper():
    index = 1
    port_com_leader = 2888
    port_elec_leader = 3888
    config = configparser.ConfigParser()
    config.read("./spark/conf.ini")
    hosts = getHostsByKey(config, "Master")

    with open(os.path.expanduser('/home/xnet/spark/conf/zoo.cfg'), 'a') as confFile:
        for host in hosts:
            subprocess.run(['echo', 'server-'+str(index)+':'+host+':'+str(port_com_leader)+':'+str(port_elec_leader)], stdout=confFile, check=True)
            index += 1
            port_com_leader += 1
            port_elec_leader += 1
    return

def define_id_zookeeper():
    id = 1
    config = configparser.ConfigParser()
    config.read("./spark/conf.ini")
    hosts = getHostsByKey(config, "Master")
    hostname = socket.gethostname()
    subprocess.run(['mkdir', '/usr/lib/zookeeper/'+zookeeper_version+'/tmp/'])
    for host in hosts:
        if host in hostname:
            with open(os.path.expanduser('/usr/lib/zookeeper/'+zookeeper_version+'/tmp/myid'), 'a') as idFile:
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

# Check if String il already present in the file
def isAlreadyAdd(pathFile,string):
    file = open(pathFile)
    for line in file:
        if string in line:
            return True
    return False

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    install_spark()
    if isMaster():
        install_zookeeper()