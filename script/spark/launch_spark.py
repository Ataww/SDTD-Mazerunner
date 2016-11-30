#!/usr/bin/env python3

import os
import logging
import subprocess

url_master = '127.0.0.1'
port_master = '7070'
port_webui = '8080'

# Function for launch Spark
def launch_spark():
    ip = os.popen('ifconfig ens3 | grep "inet ad" | cut -f2 -d: | awk \'{print $1}\'', "r").read()
    file = open('./spark/master.txt')
    for host in file:
        if host in ip:
            url_master = host.split('/n')[0]
            launch_master(url_master)
    file.close()
    file = open('./spark/slave.txt')
    for host in file:
        if host in ip:
            launch_slave()
    file.close()
    return

# Function for launch master
def launch_master(url):
    logging.info(" Start Spark Master ...")
    subprocess.run(['stop-master.sh'])
    subprocess.run(['start-master.sh','-i',url,'-p',port_master,'--webui-port',port_webui])
    return


# Function for launch slave
def launch_slave():
    logging.info(" Start Spark Worker ...")
    subprocess.run(['stop-slave.sh'])
    subprocess.run(['start-slave.sh','spark://'+get_Ip_Master()+':'+port_master])
    return

# Function for recover the address of master
def get_Ip_Master():
    file = open('./spark/master.txt')
    for host in file:
        ip_master = host.split('/n')[0]
        return ip_master

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    launch_spark()