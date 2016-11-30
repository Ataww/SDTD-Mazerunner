#!/usr/bin/env python3

import subprocess, os, sys, logging

version='hadoop-2.7.3'
distrib='http://apache.crihan.fr/dist/hadoop/common/'+version+'/'+version+'.tar.gz'


def install_hdfs():
	"""Install hadoop et set it up"""
	logging.info('Downloading hadoop')
	subprocess.run(['wget', distrib], check=True)
	logging.info('Uncompressing to /opt/')
	subprocess.run(['tar', 'xf', version+'tar.gz', '/opt/'], check=True)
	logging.info('Creating symbolic links')
	subprocess.run(['ln', '-s', '/opt/'+version+'/bin/hdfs', '/bin/hdfs'])
	subprocess.run(['ln', '-s', '/opt/'+version+'/sbin/start-dfs.sh', '/sbin/start-dfs.sh'])
	subprocess.run(['ln', '-s', '/opt/'+version+'/sbin/stop-dfs.sh', '/sbin/stop-dfs.sh'])
	logging.info('Cleaning the fuck up')
	subprocess.run(['rm', '-rf', version+'tar.gz'])	

	# TODO modifier les fichiers de conf

def install_zookeeper():
	pass

if __name__ == '__main__':
	if os.getuid() != 0:
		print('Root permissions required', file=sys.stderr)
		sys.exit(1)
	logging.basicConfig(level=logging.INFO)
	install_hdfs()