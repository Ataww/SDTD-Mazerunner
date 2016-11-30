#!/usr/bin/env python3

import os
import logging
import subprocess

spark_version = 'spark-2.0.2-bin-hadoop2.7'


# Function for install Spark and its environment
def install_spark():
    SPARK_STATUS = os.popen('stop-master.sh 2>&1 ', "r").read()
    if 'not found' in SPARK_STATUS:
        logging.info(" Downloading Spark ...")
        out = subprocess.run(['wget','-q','http://d3kbcqa49mib13.cloudfront.net/'+spark_version+'.tgz'], check=True)
        if out.returncode == 0:
            logging.info(" Downloading Spark with success")
        logging.info(" Installation of Spark ...")
        subprocess.run(['sudo','rm','-rf','/usr/lib/spark'])
        subprocess.run(['sudo','mkdir','/usr/lib/spark'])
        out = subprocess.run(['sudo','tar','-xf',spark_version+'.tgz','-C','/usr/lib/spark'], check=True)
        if out.returncode == 0:
            logging.info(" Uncompressing Spark with success")
        subprocess.run(['rm',spark_version+'.tgz'])
        # TODO use subprocess
        #subprocess.run(['echo','export PATH=$PATH:/usr/lib/spark/'+spark_version+'/sbin/','>>','~/.profile'])
        #subprocess.run(['echo','export SPARK_HOME=/usr/lib/spark/'+spark_version+'','>>','~/.profile'])
        os.system('echo "export PATH=$PATH:/usr/lib/spark/'+spark_version+'/sbin/" >> ~/.profile')
        os.system('echo "export SPARK_HOME=/usr/lib/spark/'+spark_version+'" >> ~/.profile')
        subprocess.run(['sudo','mkdir','/usr/lib/spark/spark-2.0.2-bin-hadoop2.7/logs'])
        subprocess.run(['sudo','chmod','777','-R','/usr/lib/spark/spark-2.0.2-bin-hadoop2.7/logs'])
        subprocess.run(['sudo','mkdir','/usr/lib/spark/spark-2.0.2-bin-hadoop2.7/work'])
        subprocess.run(['sudo','chmod','777','-R','/usr/lib/spark/spark-2.0.2-bin-hadoop2.7/work'])
        # TODO add log for know if spark is installed
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    install_spark()
