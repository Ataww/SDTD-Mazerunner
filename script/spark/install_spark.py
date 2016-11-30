#!/usr/bin/env python3

import os

spark_version = 'spark-2.0.2-bin-hadoop2.7'


# Function for install Spark and its environment
def install_spark():
    os.system(' echo "#############################"')
    os.system(' echo "####### Install Spark #######"')
    os.system(' echo "#############################"')
    os.system(' echo "[Info] Download Spark"')
    os.system('wget http://d3kbcqa49mib13.cloudfront.net/'+spark_version+'.tgz')
    os.system('sudo rm -rf /usr/lib/spark')
    os.system('sudo mkdir /usr/lib/spark')
    os.system('sudo tar xf '+spark_version+'.tgz -C /usr/lib/spark/')
    os.system('rm '+spark_version+'.tgz')
    os.system('echo "export PATH=$PATH:/usr/lib/spark/'+spark_version+'/sbin/" >> ~/.profile')
    os.system('echo "export SPARK_HOME=/usr/lib/spark/'+spark_version+'" >> ~/.profile')
    os.system('sudo mkdir /usr/lib/spark/spark-2.0.2-bin-hadoop2.7/logs')
    os.system('sudo chmod 777 -R /usr/lib/spark/spark-2.0.2-bin-hadoop2.7/logs/')
    os.system('sudo mkdir /usr/lib/spark/spark-2.0.2-bin-hadoop2.7/work')
    os.system('sudo chmod 777 -R /usr/lib/spark/spark-2.0.2-bin-hadoop2.7/work/')
    return

#install_spark()
