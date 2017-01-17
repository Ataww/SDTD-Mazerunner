#!/usr/bin/env python3

import configparser
import logging
import os
import socket
import subprocess

java_export = 'JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64'


# Function for install python2.7
def install_python():
    PYTHON_VERSION = os.popen('python -V 2>&1 |awk \'{ print $2 }\'', "r").read()
    if '2.7' not in PYTHON_VERSION:
        logging.info("Installation of python ...")
        out = os.system("sudo apt-get -qq -y install python >> /dev/null 2>&1")
        if out == 0:
            logging.info("Python 2.7 installed [success]")
        else:
            logging.error("Python installation failed [error]")
    return


# Function for install Java
def install_java():
    JAVA_VERSION = os.popen('java -version 2>&1 |awk \'NR==1{ gsub(/"/,""); print $3 }\'', "r").read()
    if '1.8.0_111' not in JAVA_VERSION:
        logging.info("Installation of OpenJDK 8")
        out = os.system("sudo apt-get update >> /dev/null 2>&1")
        out = os.system("sudo apt-get -qq -y install openjdk-8-jdk >> /dev/null 2>&1")
        if not lib.isAlreadyAdd('/etc/environment', java_export):
            os.system('echo ' + java_export + ' | sudo tee -a /etc/environment >> /dev/null 2>&1')

        if out == 0:
            logging.info("OpenJDK 8 installed [success]")
        else:
            logging.error("OpenJDK 8 installation failed [error]")
    return


# Function for install pika
def install_pika():
    PYTHON_PIKA_STATUS = os.popen('apt-cache policy python-pika | grep Installed', "r").read()
    if "Installed: (none)" in PYTHON_PIKA_STATUS:
        logging.info("Installation of python-pika")
        out = subprocess.run(['sudo', 'apt-get', '-qq', '-y', 'install', 'python-pika'], stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        if out.returncode == 0:
            logging.info("python-pika installed [success]")
        else:
            logging.error("python-pika installation failed [error]")
    return


# Function for define the hostname
def define_hostname():
    components = ['hdfs', 'neo4j', 'rabbitmq', 'spark', 'zookeeper']
    current_ip = lib.getIp()
    hostname = ''

    for component in components:
        hosts = lib.getHostsByKey(config, component)
        index = 1
        for host in hosts:
            if not lib.isAlreadyAdd("/etc/hosts", host + ' ' + component + '-' + str(index)):
                os.system('echo "' + host + ' ' + component + '-' + str(
                    index) + '" | sudo tee -a /etc/hosts >> /dev/null 2>&1')
            if host in current_ip:
                if '' == hostname:
                    hostname = component + '-' + str(index)
                elif component not in hostname:
                    hostname = component + '-' + str(index) + '-' + hostname
            index += 1

    if lib.isAlreadyAdd("/etc/hosts", hostname):
        lib.deleteLineWithString("/etc/hosts", hostname)

    os.system('echo "' + hostname + '" | sudo tee /etc/hostname >> /dev/null 2>&1')
    os.system('sudo hostname ' + hostname + ' >> /dev/null 2>&1')
    os.system('echo "' + lib.getIp() + ' ' + hostname + '" | sudo tee -a /etc/hosts >> /dev/null 2>&1')

    logging.info("Finished to defined hostname for this machine")
    return


# Function to define known_hosts file
def define_know_host():
    logging.info("Define known_hosts")
    components = ['hdfs', 'neo4j', 'rabbitmq', 'spark']
    os.system('cp ~/.ssh/xnet ~/.ssh/id_rsa >> /dev/null 2>&1')
    os.system('cp ~/.ssh/xnet.pub ~/.ssh/id_rsa.pub >> /dev/null 2>&1')
    os.system('rm ~/.ssh/known_hosts >> /dev/null 2>&1')
    os.system('touch ~/.ssh/known_hosts >> /dev/null 2>&1')
    for component in components:
        hosts = lib.getHostsByKey(config, component)
        index = 1
        for host in hosts:
            os.system('ssh-keyscan -t rsa ' + component + '-' + str(index) + ' >> ~/.ssh/known_hosts 2>&1')
            index += 1
    os.system('ssh-keyscan -t rsa ' + socket.gethostname() + ' >> ~/.ssh/known_hosts 2>&1')
    os.system('ssh-keyscan -t rsa 0.0.0.0 >> ~/.ssh/known_hosts 2>&1')


def install_monit():
    '''Ensures monit is installed'''
    p = subprocess.Popen(['which', 'monit'],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if '/usr/bin/monit' not in p.stdout.read().decode("utf-8").strip(' \n'):
        logging.info('Installing monit')
        if os.system('sudo apt-get -qq -y install monit >> /dev/null 2>&1'):
            logging.error('monit installation failed [error]')
        else:
            logging.info('monit installed [success]')

        # cfg bit for monit web interface
        monit_httpd_conf = 'set httpd port 2812 and allow admin:admin'

        os.system('echo ' + monit_httpd_conf + ' | sudo tee --append /etc/monit/monitrc >> /dev/null 2>&1')

        os.system('sudo monit reload >> /dev/null 2>&1')


def install_flask():
    p = subprocess.Popen(['pip3', '-V'],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if "pip 8.1.1" not in p.stdout.read().decode("utf-8").strip(' \n'):
        logging.info('Installing pip3')
        os.system("sudo apt -qq -y install python3-pip >> /dev/null 2>&1")
        p = subprocess.Popen(['pip3', 'list'],
                             stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

        if "Flask" not in p.stdout.read().decode("utf-8").strip(' \n'):
            logging.info('Installing Flask')
            subprocess.run(['pip3', 'install', 'flask'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == '__main__':
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from script.lib import lib

    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")
    config = configparser.ConfigParser()
    config.read("conf.ini")

    define_know_host()
    define_hostname()
    install_python()
    install_java()
    install_pika()
    install_monit()
    install_flask()
