#!/usr/bin/env python3

import logging
import subprocess
import configparser
import os


# Function for copy the different script on the different machine
def install_web_site():
    print("#############################################################")
    print("##### Installation of environment for the application #######")
    print("#############################################################")
    logging.info("Start to transfert file ...")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    host = getHostsByKey(config, 'application')[0]
    out = subprocess.run(['tar', 'czf', '/tmp/SDTD-Mazerunner-Backend.tar.gz', '.'],
                         cwd=os.getcwd().replace("/script", ""), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         check=True)
    if out.returncode == 0:
        logging.info("Compressing directory done [success]")
    else:
        logging.error("Compressing directory failed [error]")
    out = subprocess.run(
        ['scp', '-pq', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', '/tmp/SDTD-Mazerunner-Backend.tar.gz',
         'xnet@' + host + ':'], check=True)
    if out.returncode == 0:
        logging.info("Transfer done [success]")
    else:
        logging.error("Transferring files failed [error]")
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + host,
                    'sudo rm -rf SDTD-Mazerunner/backend/'])
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + host,
                    'mkdir -p SDTD-Mazerunner/backend/'])
    logging.info("Detar file ...")
    out = subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + host,
                          'tar xzf SDTD-Mazerunner-Backend.tar.gz -C SDTD-Mazerunner/backend/'])
    if out.returncode == 0:
        logging.info("Decompressing directory done [success]")
    else:
        logging.error("Decompressing directory failed [error]")

    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + host, 'rm -rf jar/'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + host, 'mkdir jar'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + host,
                    'mv SDTD-Mazerunner/backend/jar/ /home/xnet/jar/'], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + host,
                    'python3 SDTD-Mazerunner/backend/script/install_environment.py'])
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
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")
    install_web_site()
