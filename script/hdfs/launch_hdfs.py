#!/usr/bin/env python3

import logging, sys, configparser, socket
from subprocess import run
from logging import info

home 		= '/home/xnet'
hadoop_dir 	= home + '/hadoop-2.7.3'



def format():
	info('Formatting ActiveNN')
	run('yes Y | '+hadoop_dir+'/bin/hdfs namenode -format -force', shell=True)


def launch():
	info('Starting ActiveNN')
	run([hadoop_dir+'/sbin/hadoop-daemon.sh', 'start', 'namenode'])

	info('Copying ActiveNN metadata to StandbyNN')
	# It has to be done from StandbyNN
	config = configparser.ConfigParser()
	config.read(home+'/hdfs/conf.ini')
	run('ssh xnet@'+config.get('standbyNN', 'host')+' \"'+hadoop_dir+'/bin/hdfs namenode -bootstrapStandby\"', shell=True)

	info('Starting StandbyNN')
	run('ssh xnet@'+config.get('standbyNN', 'host')+' \"'+hadoop_dir+'/sbin/hadoop-daemon.sh start namenode\"', shell=True)

	info('Formatting ZKFC')
	run([hadoop_dir+'/bin/hdfs', 'zkfc', '-formatZK'], check=True)
	
	info('Starting ZKFCs and DNs')
	run([hadoop_dir+'/sbin/start-dfs.sh'], check=True)


def isActiveNN():
	config = configparser.ConfigParser()
	config.read('/home/xnet/SDTD-Mazerunner/script/hdfs/conf.ini')
	return config.get('activeNN', 'host') in socket.gethostname()


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

	if isActiveNN():
		format()
		launch()


