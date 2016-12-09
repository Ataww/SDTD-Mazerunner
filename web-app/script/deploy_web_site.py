#!/usr/bin/env python3

import logging
import subprocess
import configparser

# Function for copy the different script on the different machine
def install_web_site():
    print("#############################################################")
    print("####### Installation of environment for the web site ########")
    print("#############################################################")
    logging.info("Start to transfert file ...")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    host = getHostsByKey(config,'web')[0]
    out = subprocess.run(['tar','czf','/tmp/SDTD-Mazerunner.tar.gz','../../../SDTD-Mazerunner'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
    if out.returncode == 0:
        logging.info("Compressing directory done [success]")
    else:
         logging.error("Compressing directory failed [error]")
    out = subprocess.run(['scp', '-pq','-o','StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', '/tmp/SDTD-Mazerunner.tar.gz', 'xnet@'+host+':~/'],check=True)
    if out.returncode == 0:
        logging.info("Transfer done [success]")
    else:
        logging.error("Transferring files failed [error]")
    logging.info("Detar file ...")
    out = subprocess.run(['ssh','-o','StrictHostKeyChecking=no','-i', '~/.ssh/xnet', 'xnet@'+host, 'tar xzf SDTD-Mazerunner.tar.gz'])
    if out.returncode == 0:
        logging.info("Decompressing directory done [success]")
    else:
        logging.error("Decompressing directory failed [error]")
    subprocess.run(['ssh','-o','StrictHostKeyChecking=no','-i', '~/.ssh/xnet', 'xnet@'+host, './SDTD-Mazerunner/web-app/script/install_environment.py'])
    return

# Recover all ip for one component. Return format ip
def getHostsByKey(config, key):
    hosts = config.get(key, "hosts").split(',')
    index = 0
    for host in hosts:
        hosts[index] = host.strip(' \n')
        index += 1
    return hosts

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    install_web_site()