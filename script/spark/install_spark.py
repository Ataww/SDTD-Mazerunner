#!/usr/bin/env python3

import os
import logging
import subprocess

spark_version = 'spark-2.0.2-bin-hadoop2.7'


# Function for install Spark and its environment
def install_spark():
    SPARK_STATUS = os.popen('stop-master 2>&1 ', "r").read()
    if 'not found' in SPARK_STATUS:
        logging.info(" Downloading Spark ...")
        out = subprocess.run(['wget','-q','http://d3kbcqa49mib13.cloudfront.net/'+spark_version+'.tgz'], check=True)
        if out.returncode == 0:
            logging.info("Spark downloaded [success]")
        logging.info(" Installation of Spark ...")
        subprocess.run(['sudo','rm','-rf','/usr/lib/spark'])
        subprocess.run(['sudo','mkdir','/usr/lib/spark'])
        out = subprocess.run(['sudo','tar','-xf',spark_version+'.tgz','-C','/usr/lib/spark'], check=True)
        if out.returncode == 0:
            logging.info("Spark unpackec [success]")
        subprocess.run(['rm',spark_version+'.tgz'])
        subprocess.run(['sudo','ln', '-s', '/usr/lib/spark/'+spark_version+'/sbin/start-master.sh', '/sbin/start-master'])
        subprocess.run(['sudo','ln', '-s', '/usr/lib/spark/'+spark_version+'/sbin/stop-master.sh', '/sbin/stop-master'])
        subprocess.run(['sudo','ln', '-s', '/usr/lib/spark/'+spark_version+'/sbin/start-slave.sh', '/sbin/start-slave'])
        subprocess.run(['sudo','ln', '-s', '/usr/lib/spark/'+spark_version+'/sbin/stop-slave.sh', '/sbin/stop-slave'])
        with open(os.path.expanduser('~/.profile'), 'a') as proFile:
            subprocess.run(['echo', 'export SPARK_HOME=/usr/lib/spark/'+spark_version], stdout=proFile, check=True)
            subprocess.run(['echo', 'export SPARK_CONF_DIR=/home/xnet/spark/conf'], stdout=proFile, check=True)
        subprocess.run(['sudo', 'cp', '/home/xnet/spark/conf/spark-env.sh', '/usr/lib/spark/spark-2.0.2-bin-hadoop2.7/conf/spark-env.sh'])
        subprocess.run(['sudo','mkdir','/usr/lib/spark/spark-2.0.2-bin-hadoop2.7/logs'])
        subprocess.run(['sudo','chmod','777','-R','/usr/lib/spark/spark-2.0.2-bin-hadoop2.7/logs'])
        subprocess.run(['sudo','mkdir','/usr/lib/spark/spark-2.0.2-bin-hadoop2.7/work'])
        subprocess.run(['sudo','chmod','777','-R','/usr/lib/spark/spark-2.0.2-bin-hadoop2.7/work'])
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
        logging.info(" Downloading Zookeeper ...")
        out = subprocess.run(['wget', '-q', 'http://www-eu.apache.org/dist/zookeeper/zookeeper-3.4.9/zookeeper-3.4.9.tar.gz'], check=True)
        if out.returncode == 0:
            logging.info(" Downloading Zookeeper with [success]")
        else:
            logging.error(" Failed to download Zookeeper [error]")
        logging.info(" Installation of Zookeeper ...")
        subprocess.run(['sudo', 'rm', '-rf', '/usr/lib/zookeeper'])
        subprocess.run(['sudo', 'mkdir', '/usr/lib/zookeeper'])
        out = subprocess.run(['sudo', 'tar', '-xf', 'zookeeper-3.4.9.tar.gz', '-C', '/usr/lib/zookeeper'], check=True)
        if out.returncode == 0:
            logging.info("Zookeeper unpacked [success]")
        else:
            logging.error(" Failed to unpack Zookeeper [error]")
        subprocess.run(['rm', 'zookeeper-3.4.9.tar.gz'])
        with open(os.path.expanduser('~/.profile'), 'a') as proFile:
            subprocess.run(['echo', 'export PATH=$PATH:/usr/lib/zookeeper/zookeeper-3.4.9/bin'], stdout=proFile, check=True)
        logging.info("Zookeeper configuration")
        set_server_value_zookeeper()
        define_id_zookeeper()
        subprocess.run(['sudo', 'cp', '/home/xnet/spark/conf/zoo.cfg', '/usr/lib/zookeeper/zookeeper-3.4.9/conf/zoo.cfg'])
        # ZOOKEEPER_STATUS = os.popen('zkServer.sh status 2>&1 ', "r").read()
        # if 'not found' in ZOOKEEPER_STATUS:
        #    logging.info(" Zookeeper is installed with [success]")
        # else:
        #    logging.error(" Zookeeper couldn't be install [error]")
    return


# Permit to know if it is master
def isMaster():
    result = False
    ip = get_ip()
    hostfile = open('./spark/master.txt')
    for host in hostfile:
        if ip in host:
            result = True
    hostfile.close()
    return result


# Permit to define the server value for the file zoo.cfg
def set_server_value_zookeeper():
    index = 1
    port_com_leader = 2888
    port_elec_leader = 3888
    hostfile = open('./spark/master.txt')
    with open(os.path.expanduser('/home/xnet/spark/conf/zoo.cfg'), 'a') as confFile:
        for host in hostfile:
            subprocess.run(['echo', 'server-'+str(index)+':'+host.strip(' \n')+':'+str(port_com_leader)+':'+str(port_elec_leader)], stdout=confFile, check=True)
            index += 1
            port_com_leader += 1
            port_elec_leader += 1
    hostfile.close()
    return

def define_id_zookeeper():
    ip = get_ip()
    id = 1
    hostfile = open('./spark/master.txt')
    subprocess.run(['mkdir', '/usr/lib/zookeeper/zookeeper-3.4.9/tmp/'])
    for host in hostfile:
        if ip in host:
            with open(os.path.expanduser('/usr/lib/zookeeper/zookeeper-3.4.9/tmp/myid'), 'a') as idFile:
                subprocess.run(['echo', str(id)], stdout=idFile, check=True)
            return
        id += 1
    hostfile.close()
    return


# Get the ip of the current machine
def get_ip():
    ip = os.popen('ifconfig ens3 | grep "inet ad" | cut -f2 -d: | awk \'{print $1}\'', "r").read()
    ip = ip.strip(' \n')
    return ip

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    install_spark()
    if isMaster():
        install_zookeeper()