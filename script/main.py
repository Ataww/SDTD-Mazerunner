#!/usr/bin/env python

import os
import logging
import subprocess

components = ['hdfs', 'neo4j', 'rabbitmq', 'spark']

# Function for copy the different script on the different machine
def install_environment():
    print("#############################################################")
    print("####### Installation of environment of all machines #########")
    print("#############################################################")
    for conponent in components:
        file = open('./'+conponent+'/hostfile.txt')
        index = 1
        for host in file:
            logging.info(" Set environment for component " + conponent + " on the machine with address " + host.replace('\n', ''))
            logging.info(' Transfer all files ... ')
            subprocess.run(['ssh', '-i', '~/.ssh/xnet', 'xnet@' + host.replace('\n', ''), 'rm -rf ' + conponent])
            subprocess.run(['scp','-pq','-i','~/.ssh/xnet','./install_config_machine.py','xnet@' + host.replace('\n','') + ':~'])
            out = subprocess.run(['scp', '-prq', '-i', '~/.ssh/xnet', './'+conponent,'xnet@' + host.replace('\n', '') + ':~/'],check=True)
            if out.returncode == 0:
                logging.info(" Transferring finish [success]")
            else:
                logging.error(" Transferring files failed [error]")
            subprocess.run(['ssh', '-i', '~/.ssh/xnet', 'xnet@' + host.replace('\n', ''),'source ~/.profile; ./install_config_machine.py '+conponent+' '+str(index)])
            subprocess.run(['ssh', '-i', '~/.ssh/xnet', 'xnet@' + host.replace('\n', ''),'source ~/.profile; ./'+conponent+'/install_'+conponent+'.py'])
            index += 1
        file.close()
    return

# Function who will launch the different component
def launch_component():
    print("############################################################")
    print("####### Launch the different component on machines #########")
    print("############################################################")
    for conponent in components:
        file = open('./'+conponent+'/hostfile.txt')
        for host in file:
            logging.info(" Launch component " + conponent + " on the machine with address " + host.replace('\n', ''))
            subprocess.run(['ssh','-i','~/.ssh/xnet','xnet@'+host.replace('\n',''),'source ~/.profile; ./'+conponent+'/launch_'+conponent+'.py'])
        file.close()
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    install_environment()
    launch_component()