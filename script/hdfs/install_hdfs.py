#!/usr/bin/env python3

import subprocess, os, sys, logging, configparser, socket

from subprocess import run
from logging import info
from os.path import exists


version = 'hadoop-2.7.3'
distrib = 'http://apache.crihan.fr/dist/hadoop/common/'+version+'/'+version+'.tar.gz'

version_zk = 'zookeeper-3.4.9'
distrib_zk = 'http://apache.crihan.fr/dist/zookeeper/'+version_zk+'/'+version_zk+'.tar.gz'

home            = '/home/xnet'

setup_dir       = home + '/hdfs' # contains the installation scripts and etc
hadoop_dir      = home + '/' + version
zookeeper_dir   = home + '/hdfs_zk'
conf_dir        = hadoop_dir + "/etc/hadoop"



def install_hdfs():
    """Install hadoop et set it up"""
    if not exists(hadoop_dir):
        info('Downloading hadoop')
        run(['wget', '-q', '-nc', distrib], check=True)

        info('Uncompressing to /home/xnet')
        run(['tar', 'xf', version + '.tar.gz', '-C', '/home/xnet'], check=True)

        info('Setting environment variables')
        with open(home + '/.profile', 'r+') as proFile:
            if "HADOOP_CONF_DIR" not in proFile.read():
                run(['echo', "export HADOOP_CONF_DIR=" + conf_dir], stdout=proFile, check=True)
                run(['echo', 'export HADOOP_PREFIX=' + hadoop_prefix], stdout=proFile, check=True)

        info('Copying HDFS configuration files')
        run('cp ' + setup_dir + '/etc/hadoop/* ' + hadoop_dir + '/etc/hadoop', shell=True)

        run(['mkdir', '-p', hadoop_dir +'/data/namenode'])

        # Remove any previous tmp files
        info('Removing any previous tmp files')
        run('rm -rf /tmp/hadoop-xnet', shell=True)

        info('Starting journalnode')
        run([hadoop_dir + '/sbin/hadoop-daemon.sh', 'start', 'journalnode'], check=True)


def install_zookeeper():
    """Install zookeeper"""
    if not exists(zookeeper_dir):
        info('Downloading ZK (hdfs)')
        run(['wget', '-q', '-nc', distrib_zk], check=True)

        info('Uncompressing to /home/xnet')
        run(['tar', 'xf', version_zk + '.tar.gz', '-C', home], check=True)
        run(['mv', home + '/' + version_zk, zookeeper_dir])

        info('Copying ZK (hdfs) configuration files')
        run('cp ' + setup_dir + '/etc/zookeeper/* ' + zookeeper_dir + '/conf', shell=True)

        info('Creating ZK (hdfs) dataDir')
        run(['mkdir', zookeeper_dir + '/tmp_data'])

        info('Setting ZK (hdfs) service id')
        with open( zookeeper_dir + '/tmp_data/myid', 'w') as myidFile:
            # get ZK server id based on the hostname (for instance spark-1-hdfs-1 is 1)
            run(['echo', socket.gethostname()[-1]], stdout=myidFile, check=True)

        info('Starting ZKQ server')
        run([zookeeper_dir + '/bin/zkServer.sh', 'start'], check=True)



def conf_monit(service):
    """Copy monit config files for service"""
    if not exists('/etc/monit'):
        logging.error('monit is not installed')
    else:
        info('Copying monit config files for'+service)
        os.system('sudo cp ' + setup_dir + '/etc/monit/' + service + ' /etc/monit/conf.d/')
        os.system('sudo monit reload')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO ,format="%(asctime)s :: %(levelname)s :: %(message)s")
    install_hdfs()
    install_zookeeper()
