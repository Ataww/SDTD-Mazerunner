#!/usr/bin/env python3

import subprocess, os, sys, logging

version='hadoop-2.7.3'
distrib='http://apache.crihan.fr/dist/hadoop/common/'+version+'/'+version+'.tar.gz'
conf_dir = "/opt/"+version+"/etc/hadoop/"
conf_dir_export = "export HADOOP_CONF_DIR="+conf_dir

def install_hdfs():
	"""Install hadoop et set it up"""
	logging.info('Downloading hadoop')
	subprocess.run(['wget', "-nc", distrib], check=True)
	logging.info('Uncompressing to /opt/')
	subprocess.run(['tar', 'xf', version+'.tar.gz', '-C', '/opt/'], check=True)
	logging.info('Creating symbolic links')
	subprocess.run(['ln', '-s', '/opt/'+version+'/bin/hdfs', '/bin/hdfs'])
	#subprocess.run(['ln', '-s', '/opt/'+version+'/sbin/start-dfs.sh', '/sbin/start-dfs.sh'])
	#subprocess.run(['ln', '-s', '/opt/'+version+'/sbin/stop-dfs.sh', '/sbin/stop-dfs.sh'])
	logging.info('Setting environment variables')
	with open(os.path.expanduser('~/.profile'), 'r+') as proFile:
		if conf_dir_export not in proFile.read():
			subprocess.run(['echo', conf_dir_export], stdout=proFile, check=True)
			#I got 'source : no such file or directory' and we do not need to source from this script
			#subprocess.run(['source', '~/.profile'])
	logging.info('Cleaning up')
	#rm is not necessary if you want to re-download just rm the tar.gz and relaunch the script
    #subprocess.run(['rm', '-rf', version+'.tar.gz'])
	logging.info('Copying HDFS configuration files')
	subprocess.run('cp -r ./etc/hadoop/* /opt/'+version+'/etc/hadoop', shell=True)

def install_zookeeper():
	pass


if __name__ == '__main__':
	if os.getuid() != 0:
		print('Root permissions required', file=sys.stderr)
		sys.exit(1)
	logging.basicConfig(level=logging.INFO)
	install_hdfs()
