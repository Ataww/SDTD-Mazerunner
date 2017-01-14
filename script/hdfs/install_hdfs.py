#!/usr/bin/env python3

import subprocess, os, sys, logging, configparser, socket
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
        subprocess.run('cp /home/xnet/SDTD-Mazerunner/script/hdfs/etc/hadoop/* ' + hadoop_prefix + '/etc/hadoop', shell=True)

        subprocess.run(['mkdir', '-p', '/home/xnet/'+version+'/data/namenode'])

        #Remove any previous tmp files
        logging.info('Removing any previous tmp files')
        subprocess.run('rm -rf /tmp/hadoop-xnet', shell=True)

        logging.info('Starting journalnode')
        subprocess.run(['/home/xnet/'+version+'/sbin/hadoop-daemon.sh', 'start', 'journalnode'], check=True)


def install_zookeeper():
    """Install zookeeper"""
    if not exists('/home/xnet/hdfs_zk'):
        logging.info('Downloading ZK (hdfs)')
        subprocess.run(['wget', '-q', '-nc', distrib_zk], check=True)
        logging.info('Uncompressing to /home/xnet')
        subprocess.run(['tar', 'xf', version_zk + '.tar.gz', '-C', '/home/xnet'], check=True)
        subprocess.run(['mv', '/home/xnet/'+version_zk, '/home/xnet/hdfs_zk'])
        logging.info('Copying ZK (hdfs) configuration files')
        subprocess.run('cp /home/xnet/SDTD-Mazerunner/script/hdfs/etc/zookeeper/* /home/xnet/hdfs_zk/conf', shell=True)
        logging.info('Creating ZK (hdfs) dataDir')
        subprocess.run(['mkdir', '/home/xnet/hdfs_zk/tmp_data'])
        logging.info('Setting ZK (hdfs) service id')
        with open('/home/xnet/hdfs_zk/tmp_data/myid', 'w') as myidFile:
            # get ZK server id based on the hostname (for instance spark-1-hdfs-1 is 1)
            subprocess.run(['echo', socket.gethostname()[-1]], stdout=myidFile, check=True)
        logging.info('Starting ZKQ server')
        subprocess.run(['/home/xnet/hdfs_zk/bin/zkServer.sh', 'start'], check=True)



def conf_monit(service):
    """Copy monit config files for service"""
    if not exists('/etc/monit'):
        logging.error('monit is not installed')
    else:
        logging.info('Copying monit config files for'+service)
        os.system('sudo cp /home/xnet/hdfs/etc/monit/'+service+' /etc/monit/conf.d/')
        os.system('sudo monit reload')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    install_hdfs()
    install_zookeeper()
