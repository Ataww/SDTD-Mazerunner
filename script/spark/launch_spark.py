#!/usr/bin/python

import os

url_master = '127.0.0.1'
port_master = '7070'
port_webui = '8080'

# Function for launch Spark
def launch_spark():
    ip = os.popen('ifconfig ens3 | grep "inet ad" | cut -f2 -d: | awk \'{print $1}\'', "r").read()
    file = open('./spark/master.txt')
    for host in file:
        if host + '\n' == ip:
            url_master = host
            launch_master()
    file.close()
    file = open('./spark/slave.txt')
    for host in file:
        if host + '\n' == ip:
            launch_slave()
    file.close()
    return

# Function for launch master
def launch_master():
    os.system(' echo "####################################"')
    os.system(' echo "####### Launch Spark Master ########"')
    os.system(' echo "####################################"')
    os.system('stop-master.sh')
    #os.system('start-master.sh -i '+url_master+' -p '+port_master+' --webui-port '+port_webui)
    return


# Function for launch slave
def launch_slave():
    os.system(' echo "####################################"')
    os.system(' echo "####### Launch Spark Worker ########"')
    os.system(' echo "####################################"')
    os.system('stop-slave.sh')
    # os.system('start-slave.sh spark://'+url_master+':'+port_master)
    return

#launch_spark()