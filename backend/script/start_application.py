#!/usr/bin/env python3

import logging
import subprocess
import configparser

# Function for copy the different script on the different machine
def launch_application():
    print("#############################################################")
    print("######      Launch the application on the machine      ######")
    print("#############################################################")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    host = getHostsByKey(config,'application')[0]
    subprocess.run(['ssh','-o','StrictHostKeyChecking=no','-i', '~/.ssh/xnet', 'xnet@'+host,'cd /home/xnet/SDTD-Mazerunner/backend/target/scala-2.10; spark-submit sdtd-mazerunner-backend_2.10-1.0.jar'])
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
    launch_application()