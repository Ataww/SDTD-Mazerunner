#!/usr/bin/env python3

import logging
import subprocess
import configparser

# Function for launch demo
def launch_demo():
    print("#############################################################")
    print("################# DEMO SDTD-Mazerunner start ################")
    print("#############################################################")
    subprocess.run(['./start_services.py'], cwd='./script/')
    config = configparser.ConfigParser()
    config.read("./web-app/script/conf.ini")
    host = getHostsByKey(config, 'web')[0]
    subprocess.run(['ssh','-o','StrictHostKeyChecking=no','-i', '~/.ssh/xnet', 'xnet@'+host, './SDTD-Mazerunner/web-app/script/start_web_site.py'])

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
    launch_demo()