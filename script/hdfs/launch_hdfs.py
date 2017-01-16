#!/usr/bin/env python3

import logging, sys, subprocess, configparser, socket


home='/home/xnet'
hadoop_dir=home+'/hadoop-2.7.3'



def format():
	logging.info('Formatting ActiveNN')
	subprocess.run('yes Y | '+hadoop_dir+'/bin/hdfs namenode -format -force', shell=True)


def launch():
	logging.info('Starting ActiveNN')
	subprocess.run([hadoop_dir+'/sbin/hadoop-daemon.sh', 'start', 'namenode'])

	logging.info('Copying ActiveNN metadata to StandbyNN')
	# has to be done from StandbyNN
	config = configparser.ConfigParser()
	config.read(home+'/hdfs/conf.ini')
	subprocess.run('ssh xnet@'+config.get('standbyNN', 'host')+' \"'+hadoop_dir+'/bin/hdfs namenode -bootstrapStandby\"', shell=True)
	logging.info('Starting StandbyNN')
	subprocess.run('ssh xnet@'+config.get('standbyNN', 'host')+' \"'+hadoop_dir+'/sbin/hadoop-daemon.sh start namenode\"', shell=True)

	logging.info('Formatting ZKFC')
	subprocess.run([hadoop_dir+'/bin/hdfs', 'zkfc', '-formatZK'], check=True)
	
	logging.info('Starting ZKFCs and DNs')
	subprocess.run([hadoop_dir+'/sbin/start-dfs.sh'], check=True)


def isActiveNN():
	config = configparser.ConfigParser()
	config.read('/home/xnet/hdfs/conf.ini')
	return config.get('activeNN', 'host') in socket.gethostname()


if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

	if isActiveNN():
		format()
		launch()


