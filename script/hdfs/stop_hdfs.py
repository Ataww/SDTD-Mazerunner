#!/usr/bin/env python3

import logging, sys, subprocess, configparser, socket


version='hadoop-2.7.3'



def stop():
	logging.info('Stopping HDFS cluster')
	subprocess.run(['/home/xnet/'+version+'/sbin/stop-dfs.sh'], check=True)

def isNameNode():
	config = configparser.ConfigParser()
	config.read("./hdfs/conf.ini")
	hosts = getHostsByKey(config, "Master")
	hostname = socket.gethostname()

	for host in hosts:
		if host in hostname:
			return True
	return False

# Recover all ip for one component. Return format ip
def getHostsByKey(config, key):
    hosts = config.get(key, "hosts").split(',')
    index = 0
    for host in hosts:
        hosts[index] = host.strip(' \n')
        index += 1
    return hosts

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

	if len(sys.argv) > 1:
		if sys.argv[1] == '-f':
			format()

	if isNameNode():
		stop()
	else:
		logging.info('Nothing to do on this machine ...')