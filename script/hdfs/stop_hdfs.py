#!/usr/bin/env python3

import logging, configparser, socket, os
from subprocess import run
from logging import info

home = '/home/xnet'
hadoop_dir = home + '/hadoop-2.7.3'
setup_dir = home + '/SDTD-Mazerunner/script/hdfs'  # contains the installation scripts and etc


def stop():
    info('Stopping HDFS on the machine')
    os.system('/home/xnet/hadoop-2.7.3/sbin/hadoop-daemon.sh stop namenode  >> /dev/null 2>&1')
    os.system('/home/xnet/hadoop-2.7.3/sbin/hadoop-daemon.sh stop journalnode  >> /dev/null 2>&1')
    os.system('/home/xnet/hadoop-2.7.3/sbin/hadoop-daemon.sh stop datanode  >> /dev/null 2>&1')
    os.system('/home/xnet/hadoop-2.7.3/sbin/hadoop-daemon.sh stop zkfc  >> /dev/null 2>&1')


def isDefaultNN():
    config = configparser.ConfigParser()
    config.read(setup_dir + '/conf.ini')
    return config.get('NameNode', 'default_active') in socket.gethostname()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

    stop()
