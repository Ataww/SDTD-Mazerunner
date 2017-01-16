#!/usr/bin/env python3

import logging, sys, subprocess, configparser, socket


home='/home/xnet'
hadoop_dir=home+'/hadoop-2.7.3'


def stop():
	logging.info('Stopping HDFS cluster')
	subprocess.run([hadoop_dir+'/sbin/stop-dfs.sh'], check=True)


def isDefaultNN():
	config = configparser.ConfigParser()
	config.read('/home/xnet/hdfs/conf.ini')
	return config.get('namenodes', 'default_host') in socket.gethostname()


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

	if isDefaultNN():
		stop()
