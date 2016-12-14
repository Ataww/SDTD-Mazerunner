#!/usr/bin/env python3

import configparser
import logging
import subprocess
from lib import getHostsByKey, hostIsUp

components = ['hdfs', 'neo4j', 'rabbitmq', 'spark']

# Function who will launch the different component
def launch_component():
    print("############################################################")
    print("###### Launch the different components on machines #########")
    print("############################################################")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    for component in components:
        hosts = getHostsByKey(config, component)
        for host in hosts:
            if hostIsUp(host):
                logging.info("Launch component " + component + " on the machine with address " + host)
                subprocess.run(['ssh','-o','StrictHostKeyChecking=no','-i','~/.ssh/xnet','xnet@'+host,'source ~/.profile; python3 '+component+'/launch_'+component+'.py'])
            else:
                logging.error("Impossible d'accéder à la machine " + host)
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    launch_component()