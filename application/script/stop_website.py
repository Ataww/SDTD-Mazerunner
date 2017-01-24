#!/usr/bin/env python3

import logging
import subprocess

# Function for copy the different script on the different machine
def launch_web_site():
    print("#############################################################")
    print("#######       STOP  the website on the machine       ########")
    print("#############################################################")
    subprocess.run(['sudo', 'systemctl', 'stop', 'webapp_mazerunner'], check=True)
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    launch_web_site()
