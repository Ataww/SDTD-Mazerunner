#!/usr/bin/env python3

import logging, configparser, socket
from subprocess import run
from logging import info

home		= '/home/xnet'
hadoop_dir	= home + '/hadoop-2.7.3'
setup_dir   = home + '/hdfs' # contains the installation scripts and etc



def stop():
	info('Stopping HDFS cluster')
	run([hadoop_dir + '/sbin/stop-dfs.sh'], check=True)


def isDefaultNN():
	config = configparser.ConfigParser()
	config.read(setup_dir + '/conf.ini')
	return config.get('NameNodes', 'default_active') in socket.gethostname()


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

	if isDefaultNN():
		stop()
