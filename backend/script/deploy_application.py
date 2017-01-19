#!/usr/bin/env python3

import logging
import subprocess
import configparser
import os
from start_application import launch_application


# Function for copy the different script on the different machine
def transfer_application(host):
    print("#############################################################")
    print("#### Transfer all fill for JobSpark for the application #####")
    print("#############################################################")
    logging.info("Start to transfert file ...")
    out = subprocess.run(['tar', 'czf', '/tmp/SDTD-Mazerunner-Backend.tar.gz', '.'],
                         cwd=os.getcwd().replace("backend/script", "artifact"), stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL,
                         check=True)
    if out.returncode == 0:
        logging.info("Compressing directory done [success]")
    else:
        logging.error("Compressing directory failed [error]")
    out = subprocess.run(
        ['scp', '-pq', '-o', 'StrictHostKeyChecking=no', '-i', '%s/.ssh/xnet' % os.path.expanduser("~"),
         '/tmp/SDTD-Mazerunner-Backend.tar.gz',
         'xnet@' + host + ':'], check=True)
    if out.returncode == 0:
        logging.info("Transfer done [success]")
    else:
        logging.error("Transferring files failed [error]")
    subprocess.run(
        ['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '%s/.ssh/xnet' % os.path.expanduser("~"), 'xnet@' + host,
         'sudo rm -rf SDTD-Mazerunner/artifact/'])
    subprocess.run(
        ['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '%s/.ssh/xnet' % os.path.expanduser("~"), 'xnet@' + host,
         'mkdir -p SDTD-Mazerunner/artifact/'])
    logging.info("Detar file ...")
    out = subprocess.run(
        ['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '%s/.ssh/xnet' % os.path.expanduser("~"), 'xnet@' + host,
         'tar xzf SDTD-Mazerunner-Backend.tar.gz -C SDTD-Mazerunner/artifact/'])
    if out.returncode == 0:
        logging.info("Decompressing directory done [success]")
    else:
        logging.error("Decompressing directory failed [error]")
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', 'xnet@' + host,
                    'rm SDTD-Mazerunner-Backend.tar.gz'])
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
    config = configparser.ConfigParser()
    config.read("conf.ini")
    host = getHostsByKey(config, 'application_active')[0]
    transfer_application(host)
    config = configparser.ConfigParser()
    config.read("conf.ini")
    host = getHostsByKey(config, 'application_standby')[0]
    transfer_application(host)
