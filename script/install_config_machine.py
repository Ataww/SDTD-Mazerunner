#!/usr/bin/python

import os

# Function for install python
def install_python():
    os.system(' echo "################################"')
    os.system(' echo "####### Install Python 3 #######"')
    os.system(' echo "################################"')
    os.system('sudo apt-get -y install python3.5')
    os.system('sudo ln -sfn python3.5 /usr/bin/python')
    return

#install_python()