#!/usr/bin/env python3

import logging
import subprocess
import os

# Function for copy the different script on the different machine
def install_environment():
    logging.info("Start to install nodeJs ...")
    subprocess.run(['sudo','apt-get','install','-y','nodejs'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
    subprocess.run(['sudo','apt-get','install','-y','nodejs-legacy'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
    logging.info("Start to install npm ...")
    subprocess.run(['sudo','apt-get','install','-y','npm'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
    logging.info("install dependencies ...")
    subprocess.run(['npm','install'],cwd='/home/xnet/SDTD-Mazerunner/application/',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    install_environment()
