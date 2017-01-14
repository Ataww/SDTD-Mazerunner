#!/usr/bin/env python3

import subprocess, os, sys, logging, configparser, socket

from subprocess import run
from logging import info
from os.path import exists


version = 'hadoop-2.7.3'
distrib = 'http://apache.crihan.fr/dist/hadoop/common/'+version+'/'+version+'.tar.gz'

version_zk = 'zookeeper-3.4.9'
distrib_zk = 'http://apache.crihan.fr/dist/zookeeper/'+version_zk+'/'+version_zk+'.tar.gz'

hadoop_prefix = '/home/xnet/' + version

conf_dir = hadoop_prefix + "/etc/hadoop"
conf_dir_export = "export HADOOP_CONF_DIR=" + conf_dir


def install_hdfs():
    """Install hadoop et set it up"""
    if not exists('/home/xnet/'+version):
        info('Downloading hadoop')
        run(['wget', '-q', '-nc', distrib], check=True)

        info('Uncompressing to /home/xnet')
        run(['tar', 'xf', version + '.tar.gz', '-C', '/home/xnet'], check=True)

        info('Setting environment variables')
        with open(os.path.expanduser('~/.profile'), 'r+') as proFile:
            if conf_dir_export not in proFile.read():
                run(['echo', conf_dir_export], stdout=proFile, check=True)
                run(['echo', 'export HADOOP_PREFIX=' + hadoop_prefix], stdout=proFile, check=True)


        info('Copying HDFS configuration files')
        # files to copy should be somewhere with the installation script
        # for now it uses a local repo
        run('cp /home/xnet/SDTD-Mazerunner/script/hdfs/etc/hadoop/* ' + hadoop_prefix + '/etc/hadoop', shell=True)

        run(['mkdir', '-p', '/home/xnet/'+version+'/data/namenode'])

        #Remove any previous tmp files
        info('Removing any previous tmp files')
        run('rm -rf /tmp/hadoop-xnet', shell=True)

        info('Starting journalnode')
        run(['/home/xnet/'+version+'/sbin/hadoop-daemon.sh', 'start', 'journalnode'], check=True)


def install_zookeeper():
    """Install zookeeper"""
    if not exists('/home/xnet/hdfs_zk'):
        info('Downloading ZK (hdfs)')
        run(['wget', '-q', '-nc', distrib_zk], check=True)

        info('Uncompressing to /home/xnet')
        run(['tar', 'xf', version_zk + '.tar.gz', '-C', '/home/xnet'], check=True)
        run(['mv', '/home/xnet/'+version_zk, '/home/xnet/hdfs_zk'])

        info('Copying ZK (hdfs) configuration files')
        run('cp /home/xnet/SDTD-Mazerunner/script/hdfs/etc/zookeeper/* /home/xnet/hdfs_zk/conf', shell=True)

        info('Creating ZK (hdfs) dataDir')
        run(['mkdir', '/home/xnet/hdfs_zk/tmp_data'])

        info('Setting ZK (hdfs) service id')
        with open('/home/xnet/hdfs_zk/tmp_data/myid', 'w') as myidFile:
            # get ZK server id based on the hostname (for instance spark-1-hdfs-1 is 1)
            run(['echo', socket.gethostname()[-1]], stdout=myidFile, check=True)

        info('Starting ZKQ server')
        run(['/home/xnet/hdfs_zk/bin/zkServer.sh', 'start'], check=True)



def conf_monit(service):
    """Copy monit config files for service"""
    if not exists('/etc/monit'):
        logging.error('monit is not installed')
    else:
        info('Copying monit config files for'+service)
        os.system('sudo cp /home/xnet/hdfs/etc/monit/'+service+' /etc/monit/conf.d/')
        os.system('sudo monit reload')


if __name__ == '__main__':
    logging.basicConfig(level=info,format="%(asctime)s :: %(levelname)s :: %(message)s")
    install_hdfs()
    install_zookeeper()
