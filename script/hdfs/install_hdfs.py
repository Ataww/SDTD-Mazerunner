#!/usr/bin/env python3

import subprocess, os, sys, logging

version='hadoop-2.7.3'
distrib='http://apache.crihan.fr/dist/hadoop/common/'+version+'/'+version+'.tar.gz'

hadoop_prefix = '/home/xnet/'+version

conf_dir = hadoop_prefix+"/etc/hadoop"
conf_dir_export = "export HADOOP_CONF_DIR="+conf_dir


def install_hdfs():
	"""Install hadoop et set it up"""
	logging.info('Downloading hadoop')
	subprocess.run(['wget', "-nc", distrib], check=True)
	logging.info('Uncompressing to /home/xnet')
	subprocess.run(['tar', 'xf', version+'.tar.gz', '-C', '/home/xnet'], check=True)
	logging.info('Setting environment variables')
	with open(os.path.expanduser('~/.profile'), 'r+') as proFile:
		if conf_dir_export not in proFile.read():
			subprocess.run(['echo', conf_dir_export], stdout=proFile, check=True)
			subprocess.run(['echo', 'export HADOOP_PREFIX='+hadoop_prefix], stdout=proFile, check=True)	
	logging.info('Copying HDFS configuration files')
	# files to copy should be somewhere with the installation script
	# for now it uses a local repo
	subprocess.run('cp SDTD-Mazerunner/script/hdfs/etc/hadoop/* /home/xnet/'+version+'/etc/hadoop', shell=True)



if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	install_hdfs()
