#!/usr/bin/env python3

import logging
import subprocess

# Function for launch demo
def launch_demo():
    print("#############################################################")
    print("############### DEMO SDTD-Mazerunner deployment #############")
    print("#############################################################")
    subprocess.run(['./launch_deployment.py'], cwd='./script/')
    subprocess.run(['./deploy_web_site.py'],cwd='./web-app/script/')



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    launch_demo()