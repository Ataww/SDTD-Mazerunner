#!/usr/bin/python

import os

components = ['hdfs', 'neo4j', 'rabbitmq', 'spark']

# Function for copy the different script on the different machine
def install_environment():
    print("#############################################################")
    print("####### Installation of environment of all machines #########")
    print("#############################################################")
    for conponent in components:
        file = open('./'+conponent+'/hostfile.txt')
        for host in file:
            print("[Info] Set environment for component " + conponent + " on the machine with address " + host.replace('\n', ''))
            print('[Info] Transfer all files ... ')
            os.system('ssh -i ~/.ssh/xnet xnet@' + host.replace('\n', '') + ' \'rm -rf ' + conponent + ' \'')
            os.system('ssh -i ~/.ssh/xnet xnet@' + host.replace('\n', '') + ' \'mkdir ' + conponent + ' \'')
            os.system('scp -pq -i ~/.ssh/xnet ./install_config_machine.py xnet@' + host.replace('\n','') + ':~')
            for fichier in os.listdir('./'+conponent):
                os.system('scp -pq -i ~/.ssh/xnet ./'+conponent+'/'+fichier+' xnet@' + host.replace('\n', '') + ':~/'+conponent+'/')
            os.system('ssh -i ~/.ssh/xnet xnet@'+host.replace('\n','')+' \'source ~/.profile; ./install_config_machine.py\'')
            os.system('ssh -i ~/.ssh/xnet xnet@'+host.replace('\n','')+' \'source ~/.profile; ./'+conponent+'/install_'+conponent+'.py\'')
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
            print("[Info] Launch component " + conponent + " on the machine with address " + host.replace('\n', ''))
            os.system('ssh -i ~/.ssh/xnet xnet@'+host.replace('\n','')+' \'source ~/.profile; ./'+conponent+'/launch_'+conponent+'.py\'')
        file.close()
    return

install_environment()
launch_component()