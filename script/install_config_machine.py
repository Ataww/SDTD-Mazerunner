#!/usr/bin/python3

import os

# Function for install python2.7
def install_python():
    PYTHON_VERSION = os.popen('python -V 2>&1 |awk \'{ print $2 }\'', "r").read()
    if '2.7' not in PYTHON_VERSION:
        os.system(' echo "################################"')
        os.system(' echo "####### Install Python #########"')
        os.system(' echo "################################"')
        os.system('sudo apt-get -y install python')
    return

# Function for install Java
def install_java():
    JAVA_VERSION = os.popen('java -version 2>&1 |awk \'NR==1{ gsub(/"/,""); print $3 }\'', "r").read()
    if JAVA_VERSION != '1.8.0_112\n':
        os.system(' echo "################################"')
        os.system(' echo "####### Install Java #########"')
        os.system(' echo "################################"')
        os.system('wget --no-cookies --no-check-certificate --header "Cookie: oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u112-b15/jdk-8u112-linux-x64.tar.gz" -O jdk-8-linux.tar.gz')
        os.system('tar xf jdk-8-linux.tar.gz')
        os.system('rm jdk-8-linux.tar.gz')
        os.system('sudo rm -rf /usr/lib/java/')
        os.system('sudo mkdir /usr/lib/java/')
        os.system('sudo mv jdk1.8.0_112/ /usr/lib/java/jdk1.8.0_112/')
        os.system('echo "export JAVA_HOME=/usr/lib/java/jdk1.8.0_112/" >> ~/.profile')
        os.system('echo "export PATH=$PATH:/usr/lib/java/jdk1.8.0_112/bin" >> ~/.profile')
    return

install_python()
install_java()