#!/usr/bin/env python3

import configparser
import logging
import subprocess
from lib import getHostsByKey, hostIsUp

components = ['hdfs', 'neo4j', 'rabbitmq', 'spark']


# Function for copy the different script on the different machine
def install_environment():
    print("#############################################################")
    print("####### Installation of environment of all machines #########")
    print("#############################################################")
    # Read configuration
    logging.info("Read global configuration")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    for component in components:
        hosts = getHostsByKey(config,component)
        for host in hosts:
            if hostIsUp(host):
                logging.info("Set environment for component " + component + " on the machine with address " + host)
                logging.info('Start to get all files ... ')
                subprocess.run(['scp','-pq','-o','StrictHostKeyChecking=no','-i','~/.ssh/xnet','./conf.ini','xnet@' + host + ':~'])
                subprocess.run(['scp','-pq','-o','StrictHostKeyChecking=no','-i','~/.ssh/xnet','./lib.py','xnet@' + host + ':~'])
                subprocess.run(['scp','-pq','-o','StrictHostKeyChecking=no','-i','~/.ssh/xnet','./install_config_machine.py','xnet@' + host + ':~'])
                subprocess.run(['ssh','-o','StrictHostKeyChecking=no','-i', '~/.ssh/xnet', 'xnet@' + host, 'sudo rm -rf ' + component])
                out = subprocess.run(['scp', '-prq','-o','StrictHostKeyChecking=no', '-i', '~/.ssh/xnet', './'+component, 'xnet@' + host + ':~/'],check=True)
                if out.returncode == 0:
                    logging.info("Transfer done [success]")
                else:
                    logging.error("Transferring files failed [error]")
                subprocess.run(['ssh', '-o','StrictHostKeyChecking=no','-i', '~/.ssh/xnet', 'xnet@' + host,'source ~/.profile; ./install_config_machine.py'])
                subprocess.run(['ssh', '-o','StrictHostKeyChecking=no','-i', '~/.ssh/xnet', 'xnet@' + host,'source ~/.profile; ./'+component+'/install_'+component+'.py'])
            else:
                logging.error("Impossible d'accéder à la machine "+host)
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    install_environment()