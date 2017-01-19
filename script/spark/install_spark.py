#!/usr/bin/env python3

import configparser
import logging
import os
import subprocess
from os.path import exists
import socket

from lib_spark import get_hostname, isMaster

spark_version = 'spark-2.0.2-bin-without-hadoop'
spark_home = 'SPARK_HOME=/usr/lib/spark/' + spark_version
spark_conf_dir = 'SPARK_CONF_DIR=/usr/lib/spark/' + spark_version + '/conf'


# Function for install Spark and its environment
def install_spark():
    SPARK_STATUS = os.popen('spark-daemon status org.apache.spark.deploy.master.Master 1 2>&1', "r").read()
    if 'not found' in SPARK_STATUS:
        logging.info("Downloading Spark ...")
        out = subprocess.run(['wget', '-q', 'http://d3kbcqa49mib13.cloudfront.net/' + spark_version + '.tgz'],
                             check=True)
        if out.returncode == 0:
            logging.info("Spark downloaded [success]")
        logging.info("Installation of Spark ...")
        subprocess.run(['sudo', 'rm', '-rf', '/usr/lib/spark'])
        subprocess.run(['sudo', 'mkdir', '/usr/lib/spark'])
        out = subprocess.run(['sudo', 'tar', '-xf', spark_version + '.tgz', '-C', '/usr/lib/spark'], check=True)
        if out.returncode == 0:
            logging.info("Spark unpacked [success]")
        subprocess.run(['rm', spark_version + '.tgz'])
        subprocess.run(
            ['sudo', 'ln', '-s', '/usr/lib/spark/' + spark_version + '/sbin/start-master.sh', '/sbin/start-master'])
        subprocess.run(
            ['sudo', 'ln', '-s', '/usr/lib/spark/' + spark_version + '/sbin/stop-master.sh', '/sbin/stop-master'])
        subprocess.run(
            ['sudo', 'ln', '-s', '/usr/lib/spark/' + spark_version + '/sbin/start-slave.sh', '/sbin/start-slave'])
        subprocess.run(
            ['sudo', 'ln', '-s', '/usr/lib/spark/' + spark_version + '/sbin/stop-slave.sh', '/sbin/stop-slave'])
        subprocess.run(
            ['sudo', 'ln', '-s', '/usr/lib/spark/' + spark_version + '/bin/spark-submit', '/bin/spark-submit'])
        subprocess.run(
            ['sudo', 'ln', '-s', '/usr/lib/spark/' + spark_version + '/sbin/spark-daemon.sh', '/sbin/spark-daemon'])
        if not isAlreadyAdd('/etc/environment', spark_home):
            os.system('echo ' + spark_home + ' | sudo tee -a /etc/environment >> /dev/null 2>&1')
        if not isAlreadyAdd('/etc/environment', spark_conf_dir):
            os.system('echo ' + spark_conf_dir + ' | sudo tee -a /etc/environment >> /dev/null 2>&1')
        subprocess.run(['sudo', 'mkdir', '/usr/lib/spark/' + spark_version + '/logs'])
        subprocess.run(['sudo', 'chmod', '777', '-R', '/usr/lib/spark/' + spark_version + '/logs'])
        subprocess.run(['sudo', 'mkdir', '/usr/lib/spark/' + spark_version + '/work'])
        subprocess.run(['sudo', 'chmod', '777', '-R', '/usr/lib/spark/' + spark_version + '/work'])
        setSparkDaemonOpts()
        setSparkDefaultsConf()
        SPARK_STATUS = os.popen('spark-daemon status org.apache.spark.deploy.master.Master 1 2>&1', "r").read()
        if 'not found' not in SPARK_STATUS:
            logging.info("Spark installed [success]")
        else:
            logging.error("Spark installation failed [error]")
    return


# Function for define spark-env.sh
def setSparkDaemonOpts():
    port = 2181
    isFirst = True
    export = 'export SPARK_DAEMON_JAVA_OPTS="-Dspark.deploy.recoveryMode=ZOOKEEPER -Dspark.deploy.zookeeper.url='
    config = configparser.ConfigParser()
    config.read("conf.ini")
    hosts = getHostsByKey(config, "Zookeeper")
    for host in hosts:
        if isFirst:
            export += host + ':' + str(port)
            isFirst = False
        else:
            export += ',' + host + ':' + str(port)

    export += ' -Dspark.deploy.zookeeper.dir=/usr/lib/spark/' + spark_version + '"'

    subprocess.run(['sudo', 'cp', '/home/xnet/SDTD-Mazerunner/script/spark/conf/spark-env.sh',
                    '/usr/lib/spark/' + spark_version + '/conf/spark-env.sh'])

    os.system(
        'echo \'export SPARK_MASTER_HOST="' + get_hostname() + '"\' | sudo tee -a /usr/lib/spark/' + spark_version + '/conf/spark-env.sh >> /dev/null 2>&1')
    os.system(
        'echo \'' + export + '\' | sudo tee -a /usr/lib/spark/' + spark_version + '/conf/spark-env.sh >> /dev/null 2>&1')

    return


# Function for define spark-defaults.conf
def setSparkDefaultsConf():
    port = 7070
    isFirst = True
    export = 'spark.master                     spark://'
    config = configparser.ConfigParser()
    config.read("conf.ini")
    hosts = getHostsByKey(config, "Master")
    for host in hosts:
        if isFirst:
            export += host + ':' + str(port)
            isFirst = False
        else:
            export += ',' + host + ':' + str(port)

    subprocess.run(['sudo', 'cp', '/home/xnet/SDTD-Mazerunner/script/spark/conf/spark-defaults.conf',
                    '/usr/lib/spark/' + spark_version + '/conf/spark-defaults.conf'])
    os.system(
        'echo ' + export + ' | sudo tee -a /usr/lib/spark/' + spark_version + '/conf/spark-defaults.conf >> /dev/null 2>&1')

    return


def conf_monit():
    """Copy monit config files for service"""
    hostname = socket.gethostname()
    config = configparser.ConfigParser()
    config.read('conf.ini')

    if not exists('/etc/monit'):
        logging.error('monit is not installed')
    else:
        if isMaster():
            key = 'Master'
        else:
            key = 'Slaves'

        index = 1
        for host in getHostsByKey(config, key=key):
            if host in hostname:
                logging.info('Copying monit config files for Spark ' + key + ' on host ' + hostname)
                os.system(
                    'sudo cp /home/xnet/SDTD-Mazerunner/script/spark/conf/MonitSpark' + key + '_' + str(index) + ' /etc/monit/conf.d/')
            index += 1
        os.system('sudo monit reload')
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
def isAlreadyAdd(pathFile, string):
    file = open(pathFile)
    for line in file:
        if string in line:
            return True
    return False


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

    install_spark()
    #conf_monit()
