#!/usr/bin/python

import os

components = ['hdfs', 'neo4j', 'rabbitmq', 'spark']

# Function for copy the different script on the different machine
def copy_script():
    print("###########################################")
    print("####### Start to prepare machines #########")
    print("###########################################")
    for conponent in components:
        print("[Info] Start prepare machine for component : "+conponent)
        file = open('./'+conponent+'/hostfile.txt')
        for host in file:
            print('[Info] Transfer on marchine : ' + host.replace('\n', ''))
            os.system('ssh -i ~/.ssh/xnet xnet@' + host.replace('\n', '') + ' \'rm -rf ' + conponent + ' \'')
            os.system('ssh -i ~/.ssh/xnet xnet@' + host.replace('\n', '') + ' \'mkdir ' + conponent + ' \'')
            os.system('scp -p -i ~/.ssh/xnet ./install_config_machine.py xnet@' + host.replace('\n','') + ':~')
            for fichier in os.listdir('./'+conponent):
                os.system('scp -p -i ~/.ssh/xnet ./'+conponent+'/'+fichier+' xnet@' + host.replace('\n', '') + ':~/'+conponent+'/')
            print('[Info] Launch script of install on marchine : ' + host.replace('\n', ''))
            os.system('ssh -i ~/.ssh/xnet xnet@'+host.replace('\n','')+' \'source ~/.profile; ./install_config_machine.py\'')
            os.system('ssh -i ~/.ssh/xnet xnet@'+host.replace('\n','')+' \'source ~/.profile; ./'+conponent+'/install_'+conponent+'.py\'')
            os.system('ssh -i ~/.ssh/xnet xnet@'+host.replace('\n','')+' \'source ~/.profile; ./'+conponent+'/launch_'+conponent+'.py\'')
        file.close()
    return

copy_script()