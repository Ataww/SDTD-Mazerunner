#!/usr/bin/env python3

import logging
import subprocess

# Function for copy the different script on the different machine
def launch_application():
    print("#############################################################")
    print("######      Launch the application on the machine      ######")
    print("#############################################################")
    #subprocess.run(['spark-submit','sdtd-mazerunner-backend_2.10-1.0.jar'],cwd='/home/xnet/SDTD-Mazerunner/backend/target/scala-2.10',stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    launch_application()