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
            logging.info("  Python 2.7 is installed with [success]")
        else:
            logging.error("  Python couldn't be install [error]")
    return

# Function for install Java
def install_java():
    JAVA_VERSION = os.popen('java -version 2>&1 |awk \'NR==1{ gsub(/"/,""); print $3 }\'', "r").read()
    if '1.8.0_112' not in JAVA_VERSION:
        logging.info(" Downloading Java ...")
        out = subprocess.run(['wget', '-q', '--no-cookies', '--no-check-certificate', '--header','Cookie: oraclelicense=accept-securebackup-cookie','http://download.oracle.com/otn-pub/java/jdk/8u112-b15/jdk-8u112-linux-x64.tar.gz'], check=True)
        if out.returncode == 0:
            logging.info(" Downloading Java with [success]")
        logging.info(" Installation of Java ...")
        subprocess.run(['sudo','rm','-rf','/usr/lib/java/'])
        subprocess.run(['sudo','mkdir','/usr/lib/java/'])
        out = subprocess.run(['sudo', 'tar', '-xf', 'jdk-8u112-linux-x64.tar.gz', '-C', '/usr/lib/java'], check=True)
        if out.returncode == 0:
            logging.info(" Uncompressing Java with [success]")
        subprocess.run(['rm','jdk-8u112-linux-x64.tar.gz'])
        subprocess.run(['sudo','ln', '-s', '/usr/lib/java/jdk1.8.0_112/bin/java', '/bin/java'])
        subprocess.run(['sudo','ln', '-s', '/usr/lib/java/jdk1.8.0_112/bin/javac', '/bin/javac'])
        subprocess.run(['sudo','ln', '-s', '/usr/lib/java/jdk1.8.0_112/bin/jar', '/bin/jar'])
        with open(os.path.expanduser('~/.profile'), 'a') as proFile:
            subprocess.run(['echo', 'export JAVA_HOME=/usr/lib/java/jdk1.8.0_112'], stdout=proFile, check=True)
        JAVA_VERSION = os.popen('java -version 2>&1 |awk \'NR==1{ gsub(/"/,""); print $3 }\'', "r").read()
        if '1.8.0_112' in JAVA_VERSION:
            logging.info(" Java is installed with [success]")
        else:
            logging.error(" Java couldn't be install [error]")
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
        os.system('sudo hostname '+conponent+'-'+index+' >> /dev/null 2>&1')
        logging.info(" Hostname update")
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    define_hostname(sys.argv[1],sys.argv[2])
    install_python()
    install_java()