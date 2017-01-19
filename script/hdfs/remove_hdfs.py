#!/usr/bin/env python3

import logging
import os
import subprocess

def remove_directory_hdfs():
    logging.info("Remove All files installed")
    os.system('/home/xnet/hadoop-2.7.3/sbin/stop-dfs.sh  >> /dev/null 2>&1')
    os.system('/home/xnet/hadoop-2.7.3/sbin/hadoop-daemon.sh stop namenode  >> /dev/null 2>&1')
    os.system('/home/xnet/hadoop-2.7.3/sbin/hadoop-daemon.sh stop journalnode  >> /dev/null 2>&1')
    os.system('/home/xnet/hadoop-2.7.3/sbin/hadoop-daemon.sh stop datanode  >> /dev/null 2>&1')
    os.system('/home/xnet/hadoop-2.7.3/sbin/hadoop-daemon.sh stop zkfc  >> /dev/null 2>&1')

    subprocess.run(['sudo', 'rm', '-rf', '/home/xnet/hadoop-2.7.3/'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

    remove_directory_hdfs()
