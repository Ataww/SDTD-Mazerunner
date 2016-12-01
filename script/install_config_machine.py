#!/usr/bin/env python3

import os
import logging
import subprocess
import sys

# Function for install python2.7
def install_python():
    PYTHON_VERSION = os.popen('python -V 2>&1 |awk \'{ print $2 }\'', "r").read()
    if '2.7' not in PYTHON_VERSION:
        logging.info(" Installation of python ...")
        out = subprocess.run(['sudo','apt-get','-qq','-y','install','python', '>>','/dev/null','2>&1'], check=True)
        if out.returncode == 0:
            logging.info(" Installing Python with success")
    return

# Function for install Java
def install_java():
    JAVA_VERSION = os.popen('java -version 2>&1 |awk \'NR==1{ gsub(/"/,""); print $3 }\'', "r").read()
    if JAVA_VERSION != '1.8.0_112\n':
        logging.info(" Downloading Java ...")
        out = subprocess.run(['wget', '-q', '--no-cookies', '--no-check-certificate', '--header','Cookie: oraclelicense=accept-securebackup-cookie','http://download.oracle.com/otn-pub/java/jdk/8u112-b15/jdk-8u112-linux-x64.tar.gz'], check=True)
        if out.returncode == 0:
            logging.info(" Downloading Java with success")
        logging.info(" Installation of Java ...")
        subprocess.run(['sudo','rm','-rf','/usr/lib/java/'])
        subprocess.run(['sudo','mkdir','/usr/lib/java/'])
        out = subprocess.run(['sudo', 'tar', '-xf', 'jdk-8u112-linux-x64.tar.gz', '-C', '/usr/lib/java'], check=True)
        if out.returncode == 0:
            logging.info(" Uncompressing Java with success")
        subprocess.run(['rm','jdk-8u112-linux-x64.tar.gz'])
        #TODO use subprocess
        #subprocess.run(['echo','export JAVA_HOME=/usr/lib/java/jdk1.8.0_112/','>>','~/.profile'])
        #subprocess.run(['echo','export PATH=$PATH:/usr/lib/java/jdk1.8.0_112/bin','>>','~/.profile'])
        os.system('echo "export JAVA_HOME=/usr/lib/java/jdk1.8.0_112/" >> ~/.profile')
        os.system('echo "export PATH=$PATH:/usr/lib/java/jdk1.8.0_112/bin" >> ~/.profile')
        # TODO add log for know if java is installed
    return

# Function for define the hostname
def define_hostname(conponent,index):
    if conponent == "hdfs":
        conponent = "spark"
    find = False
    file = open('/etc/hosts')
    for line in file:
        if '127.0.1.1' in line:
            find = True
    if not find:
        os.system('echo "127.0.1.1 '+conponent+'-'+index+'" | sudo tee -a /etc/hosts >> /dev/null 2>&1')
        #TODO try with subprocess
        #subprocess.run(['echo','127.0.1.1 ',conponent+'-'+index,'|','sudo','tee','-a','/etc/hosts','>>','/dev/null'])
        subprocess.run(['sudo','hostname',conponent+'-'+index],'>>','/dev/null','2>&1')
        logging.info(" Hostname update")
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    define_hostname(sys.argv[1],sys.argv[2])
    install_python()
    install_java()