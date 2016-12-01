#!/usr/bin/env python3

import os
import logging
import subprocess

spark_version = 'spark-2.0.2-bin-hadoop2.7'


# Function for install Spark and its environment
def install_spark():
    SPARK_STATUS = os.popen('stop-master 2>&1 ', "r").read()
    if 'not found' in SPARK_STATUS:
        logging.info(" Downloading Spark ...")
        out = subprocess.run(['wget','-q','http://d3kbcqa49mib13.cloudfront.net/'+spark_version+'.tgz'], check=True)
        if out.returncode == 0:
            logging.info(" Downloading Spark with [success]")
        logging.info(" Installation of Spark ...")
        subprocess.run(['sudo','rm','-rf','/usr/lib/spark'])
        subprocess.run(['sudo','mkdir','/usr/lib/spark'])
        out = subprocess.run(['sudo','tar','-xf',spark_version+'.tgz','-C','/usr/lib/spark'], check=True)
        if out.returncode == 0:
            logging.info(" Uncompressing Spark with [success]")
        subprocess.run(['rm',spark_version+'.tgz'])
        subprocess.run(['sudo','ln', '-s', '/usr/lib/spark/'+spark_version+'/sbin/start-master.sh', '/sbin/start-master'])
        subprocess.run(['sudo','ln', '-s', '/usr/lib/spark/'+spark_version+'/sbin/stop-master.sh', '/sbin/stop-master'])
        subprocess.run(['sudo','ln', '-s', '/usr/lib/spark/'+spark_version+'/sbin/start-slave.sh', '/sbin/start-slave'])
        subprocess.run(['sudo','ln', '-s', '/usr/lib/spark/'+spark_version+'/sbin/stop-slave.sh', '/sbin/stop-slave'])
        with open(os.path.expanduser('~/.profile'), 'a') as proFile:
            subprocess.run(['echo', 'export SPARK_HOME=/usr/lib/spark/'+spark_version], stdout=proFile, check=True)
        subprocess.run(['sudo','mkdir','/usr/lib/spark/spark-2.0.2-bin-hadoop2.7/logs'])
        subprocess.run(['sudo','chmod','777','-R','/usr/lib/spark/spark-2.0.2-bin-hadoop2.7/logs'])
        subprocess.run(['sudo','mkdir','/usr/lib/spark/spark-2.0.2-bin-hadoop2.7/work'])
        subprocess.run(['sudo','chmod','777','-R','/usr/lib/spark/spark-2.0.2-bin-hadoop2.7/work'])
        SPARK_STATUS = os.popen('stop-master 2>&1 ', "r").read()
        if 'not found' not in SPARK_STATUS:
            logging.info(" Spark is installed with [success]")
        else:
            logging.error(" Spark couldn't be install [error]")
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    install_spark()
