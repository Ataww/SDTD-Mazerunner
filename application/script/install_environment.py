#!/usr/bin/env python3

import logging
import subprocess
import os

# Function for copy the different script on the different machine
def install_environment():
    print("#############################################################")
    print("#######      Install environment for the WEB_APP     ########")
    print("#############################################################")
    logging.info("Start to install nodeJs ...")
    subprocess.run(['sudo','apt-get','install','-y','nodejs'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
    subprocess.run(['sudo','apt-get','install','-y','nodejs-legacy'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
    logging.info("Start to install npm ...")
    subprocess.run(['sudo','apt-get','install','-y','npm'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
    logging.info("install dependencies ...")
    subprocess.run(['npm','install'],cwd='/home/xnet/SDTD-Mazerunner/application/',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    subprocess.run(['npm','install', 'http'],cwd='/home/xnet/SDTD-Mazerunner/application/',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'rm', '/etc/systemd/system/webapp_mazerunner.service'], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'cp', '/home/xnet/SDTD-Mazerunner/application/script/webapp_mazerunner.service',
                    '/etc/systemd/system/'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'systemctl', 'enable', 'webapp_mazerunner'], stdout=subprocess.DEVNULL,
                  stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'systemctl', 'daemon-reload'], stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    install_environment()
