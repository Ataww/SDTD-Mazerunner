#!/usr/bin/env python3

import logging, sys, configparser, socket
from subprocess import run
from logging import info

home		= '/home/xnet'
hadoop_dir	= home + '/hadoop-2.7.3'


def stop():
	info('Stopping HDFS cluster')
	run([hadoop_dir+'/sbin/stop-dfs.sh'], check=True)


def isDefaultNN():
	config = configparser.ConfigParser()
	config.read('/home/xnet/SDTD-Mazerunner/script/hdfs/conf.ini')
	return config.get('namenodes', 'default_host') in socket.gethostname()


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

	if isDefaultNN():
		stop()
