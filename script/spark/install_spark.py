#!/usr/bin/env python3

import os

url_master = '127.0.0.1'
port_master = '7070'
port_webui = '8080'
spark_version = 'spark-2.0.2-bin-hadoop2.7'


# Function for install Spark and its environment
def install_spark():
    # os.system(' echo "#############################"')
    # os.system(' echo "####### Install Spark #######"')
    # os.system(' echo "#############################"')
    # os.system(' echo "[Info] Download Spark"')
    # os.system('wget http://d3kbcqa49mib13.cloudfront.net/'+spark_version+'.tgz')
    # os.system('sudo rm -rf /usr/lib/spark')
    # os.system('sudo mkdir /usr/lib/spark')
    # os.system('sudo tar xf '+spark_version+'.tgz -C /usr/lib/spark/')
    # os.system('rm '+spark_version+'.tgz')
    # os.system('echo "export PATH=$PATH:/usr/lib/spark/'+spark_version+'/sbin/" >> ~/.bashrc')
    # os.system('export PATH=$PATH:/usr/lib/spark/'+spark_version+'/sbin/')
    # os.system('echo "export SPARK_HOME/usr/lib/spark/'+spark_version+'/bin/" >> ~/.bashrc')
    # os.system('export SPARK_HOME/usr/lib/spark/'+spark_version+'/bin/')
    # os.system('sudo mkdir /usr/lib/spark/spark-2.0.2-bin-hadoop2.7/logs')
    # os.system('sudo chmod 777 -R /usr/lib/spark/spark-2.0.2-bin-hadoop2.7/logs/')
    # os.system('sudo mkdir /usr/lib/spark/spark-2.0.2-bin-hadoop2.7/work')
    # os.system('sudo chmod 777 -R /usr/lib/spark/spark-2.0.2-bin-hadoop2.7/work/')
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
    os.system('start-master.sh -i '+url_master+' -p '+port_master+' --webui-port '+port_webui)
    return


# Function for launch slave
def launch_slave():
    os.system(' echo "####################################"')
    os.system(' echo "####### Launch Spark Worker ########"')
    os.system(' echo "####################################"')
    os.system('stop-slave.sh')
    # os.system('start-slave.sh spark://'+url_master+':'+port_master)
    return


#install_spark()
