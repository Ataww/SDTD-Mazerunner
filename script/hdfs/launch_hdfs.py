#!/usr/bin/env python3

import logging, sys, configparser, socket
from subprocess import run
from logging import info

home = '/home/xnet'
hadoop_dir = home + '/hadoop-2.7.3'
setup_dir = home + '/SDTD-Mazerunner/script/hdfs'  # contains the installation scripts and etc


def format():
    info('Formatting the active NN')
    run('yes Y | ' + hadoop_dir + '/bin/hdfs namenode -format -force', shell=True)


def launch():
    info('Starting active NN')
    run([hadoop_dir + '/sbin/hadoop-daemon.sh', 'start', 'namenode'])

    info('Copying active NN metadata to standby NN')
    # It has to be done from StandbyNN
    config = configparser.ConfigParser()
    config.read(setup_dir + '/conf.ini')
    run('ssh xnet@' + config.get('NameNode',
                                 'default_standby') + ' \"' + hadoop_dir + '/bin/hdfs namenode -bootstrapStandby\"',
        shell=True)

    info('Starting standby NN')
    run('ssh xnet@' + config.get('NameNode',
                                 'default_standby') + ' \"' + hadoop_dir + '/sbin/hadoop-daemon.sh start namenode\"',
        shell=True)

    info('Formatting ZKFC')
    run([hadoop_dir + '/bin/hdfs', 'zkfc', '-formatZK', '-force'], check=True)

    info('Starting ZKFCs and DNs')
    run([hadoop_dir + '/sbin/start-dfs.sh'], check=True)


def isActiveNN():
    config = configparser.ConfigParser()
    config.read(setup_dir + '/conf.ini')
    return config.get('NameNode', 'default_active') in socket.gethostname()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

    if isActiveNN():
        format()
        launch()
