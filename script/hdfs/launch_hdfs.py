#!/usr/bin/env python3

import logging, sys, subprocess


version='hadoop-2.7.3'


def format():
	logging.info('Formatting HDFS namenode')
	subprocess.run(['/home/xnet/'+version+'/bin/hdfs', 'namenode', '-format'], check=True)


def launch():
	logging.info('Launching HDFS cluster')
	subprocess.run(['/home/xnet/'+version+'/sbin/start-dfs.sh'], check=True)


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	
	if len(sys.argv) > 1:
		if sys.argv[1] == '-f':
			format()

	launch()