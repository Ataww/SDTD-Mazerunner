#!/usr/bin/python3

import os

# Function for install python
def install_python():
    os.system(' echo "################################"')
    os.system(' echo "####### Install Python #########"')
    os.system(' echo "################################"')
    os.system('sudo apt-get -y install python')
    return

install_python()