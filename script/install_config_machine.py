#!/usr/bin/env python3

import os
import logging
import subprocess
import configparser
import socket

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
        if not isAlreadyAdd('/etc/environment',java_export):
            os.system('echo '+java_export+' | sudo tee -a /etc/environment >> /dev/null 2>&1')

        if out == 0:
            logging.info("OpenJDK 8 installed [success]")
        else:
            logging.error("OpenJDK 8 installation failed [error]")
    return

# Function for install pika
def install_pika():
    PYTHON_PIKA_STATUS = os.popen('apt-cache policy python-pika | grep Installed', "r").read()
    if "Installed" not in PYTHON_PIKA_STATUS:
        logging.info("Installation of python-pika")
        out = subprocess.run(['sudo', 'apt-get','-qq','-y', 'install', 'python-pika'], check=True)
        if out.returncode == 0:
            logging.info("python-pika installed [success]")
        else:
            logging.error("python-pika installation failed [error]")
    return

# Function for define the hostname
def define_hostname():

    components = ['hdfs', 'neo4j', 'rabbitmq', 'spark']
    current_ip = get_ip()
    hostname = ''

    config = configparser.ConfigParser()
    config.read("conf.ini")

    for component in components:
        hosts = getHostsByKey(config,component)
        index = 1
        for host in hosts:
            if not isAlreadyAdd("/etc/hosts",host + ' ' + component + '-' + str(index)):
                os.system('echo "' + host + ' ' + component + '-' + str(index) + '" | sudo tee -a /etc/hosts >> /dev/null 2>&1')
            if host in current_ip:
                if '' == hostname:
                    hostname = component + '-' + str(index)
                elif component not in hostname:
                    hostname = component + '-' + str(index) + '-' + hostname
            index += 1

    if isAlreadyAdd("/etc/hosts",hostname):
        deleteLineWithString("/etc/hosts",hostname)

    os.system('echo "' + hostname + '" | sudo tee /etc/hostname >> /dev/null 2>&1')
    os.system('sudo hostname ' + hostname + ' >> /dev/null 2>&1')
    os.system('echo "'+get_ip()+' '+ hostname + '" | sudo tee -a /etc/hosts >> /dev/null 2>&1')

    logging.info("Finished to defined hostname for this machine")
    return

# Function who return the ip of the current machine
def get_ip():
    ip = os.popen('ifconfig ens3 | grep "inet ad" | cut -f2 -d: | awk \'{print $1}\'', "r").read()
    ip = ip.replace('\n', '')
    return ip

# Check if String il already present in the file
def isAlreadyAdd(pathFile,string):
    file = open(pathFile)
    for line in file:
        if string in line:
            return True
    return False

# Recover all ip for one component. Return format ip
def getHostsByKey(config, key):
    hosts = config.get(key, "hosts").split(',')
    index = 0
    for host in hosts:
        hosts[index] = host.strip(' \n')
        index += 1
    return hosts

def deleteLineWithString(pathFile,stringResearch):

    contenu = ""
    fichier = open(pathFile, "r")
    for ligne in fichier:
        if not (stringResearch in ligne):
            contenu += ligne
    fichier.close()

    fichier = open('tmp.txt', 'w')
    fichier.write(contenu)
    fichier.close()
    os.system('sudo mv tmp.txt /etc/hosts >> /dev/null 2>&1')
    return

# Function to define known_hosts file

def define_know_host():
    logging.info("Define known_hosts")
    components = ['hdfs', 'neo4j', 'rabbitmq', 'spark']
    os.system('cp ~/.ssh/xnet ~/.ssh/id_rsa >> /dev/null 2>&1')
    os.system('cp ~/.ssh/xnet.pub ~/.ssh/id_rsa.pub >> /dev/null 2>&1')
    os.system('rm ~/.ssh/known_hosts >> /dev/null 2>&1')
    os.system('touch ~/.ssh/known_hosts >> /dev/null 2>&1')
    config = configparser.ConfigParser()
    config.read("conf.ini")
    for component in components:
        hosts = getHostsByKey(config, component)
        index = 1
        for host in hosts:
            os.system('ssh-keyscan -t rsa ' + component + '-' + str(index) + ' >> ~/.ssh/known_hosts 2>&1')
            index += 1
    os.system('ssh-keyscan -t rsa ' + socket.gethostname() + ' >> ~/.ssh/known_hosts 2>&1')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    define_know_host()
    define_hostname()
    install_python()
    install_java()
    install_pika()
