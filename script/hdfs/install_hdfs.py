#!/usr/bin/env python3

import subprocess, os, sys, logging, configparser, socket
from os.path import exists


version = 'hadoop-2.7.3'
distrib = 'http://apache.crihan.fr/dist/hadoop/common/'+version+'/'+version+'.tar.gz'

version_zk = 'zookeeper-3.4.9'
distrib_zk = 'http://apache.crihan.fr/dist/zookeeper/'+version+'/'+version+'.tar.gz'

hadoop_prefix = '/home/xnet/' + version

conf_dir = hadoop_prefix + "/etc/hadoop"
conf_dir_export = "export HADOOP_CONF_DIR=" + conf_dir

def format_hdfs():
	logging.info('Formatting HDFS namenode')
	subprocess.run(['/home/xnet/'+version+'/bin/hdfs', 'namenode', '-format', '-force'], check=True)

def isNameNode():
	config = configparser.ConfigParser()
	config.read("/home/xnet/hdfs/conf.ini")
	hosts = getHostsByKey(config, "Master")
	hostname = socket.gethostname()

	for host in hosts:
		if host in hostname:
			return True
	return False

def getHostsByKey(config, key):
    """Recover all ips for one component. Return format ip"""
    hosts = config.get(key, "hosts").split(',')
    index = 0
    for host in hosts:
        hosts[index] = host.strip(' \n')
        index += 1
    return hosts

def install_hdfs():
    """Install hadoop et set it up"""
    if not exists('/home/xnet/'+version):
        logging.info('Downloading hadoop')
        subprocess.run(['wget', '-q', '-nc', distrib], check=True)
        logging.info('Uncompressing to /home/xnet')
        subprocess.run(['tar', 'xf', version + '.tar.gz', '-C', '/home/xnet'], check=True)
        logging.info('Setting environment variables')
        with open(os.path.expanduser('~/.profile'), 'r+') as proFile:
            if conf_dir_export not in proFile.read():
                subprocess.run(['echo', conf_dir_export], stdout=proFile, check=True)
                subprocess.run(['echo', 'export HADOOP_PREFIX=' + hadoop_prefix], stdout=proFile, check=True)


        logging.info('Copying HDFS configuration files')
        # files to copy should be somewhere with the installation script
        # for now it uses a local repo
        subprocess.run('cp /home/xnet/hdfs/etc/hadoop/* ' + hadoop_prefix + '/etc/hadoop', shell=True)

        #Remove any previous tmp files
        logging.info('Removing any previous tmp files')
        subprocess.run('rm -rf /tmp/hadoop-xnet', shell=True)

        if isNameNode():
            #Format the HDFS partition
            logging.info('Format the HDFS partition')
            format_hdfs()


def install_zookeeper():
    """Install zookeeper"""
    if not exists('/home/xnet/hdfs_zk'):
        logging.info('Downloading ZK (hdfs)')
        subprocess.run(['wget', '-q', '-nc', distrib_zk])
        logging.info('Uncompressing to /home/xnet')
        subprocess.run(['tar', 'xf', version_zk + '.tar.gz', '-C', '/home/xnet'], check=True)
        subprocess.run(['mv', '/home/xnet/'+version_zk, '/home/xnet/hdfs_zk'])
        logging.info('Copying ZK (hdfs) configuration files')
        subprocess.run('cp /home/xnet/hdfs/etc/zookeeper/* ' + 'home/xnet/hdfs_zk/conf', shell=True)
        logging.info('Creating ZK (hdfs) dataDir')
        subprocess.run(['rm', '-rf', '/home/xnet/hdfs_zk/tmp_data'], check=True)
        subprocess.run(['/home/xnet/hdfs_zk/tmp_data'], check=True)
        logging.info('Setting ZK (hdfs) service id')
        with open('/home/xnet/hdfs_zk/tmp_data', 'w') as myidFile:
            # get ZK server id based on the hostname (for instance spark-1-hdfs-1 is 1)
            subprocess.run(['echo', socket.gethostname()[-1]], stdout=myidFile, check=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    install_hdfs()
    install_zookeeper()
