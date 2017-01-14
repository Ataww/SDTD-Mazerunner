#!/usr/bin/env python3

import subprocess
import os

spark_home = 'SPARK_HOME'
spark_conf_dir = 'SPARK_CONF_DIR'


def remove_directory_spark():
    subprocess.run(['sudo', 'rm', '-rf', '/usr/lib/spark'])
    subprocess.run(['sudo', 'rm', '/sbin/stop-master'])
    subprocess.run(['sudo', 'rm', '/sbin/stop-slave'])
    subprocess.run(['sudo', 'rm', '/sbin/start-master'])
    subprocess.run(['sudo', 'rm', '/sbin/start-slave'])
    subprocess.run(['sudo', 'rm', '/bin/spark-submit'])
    return


def remove_directory_zookeeper():
    subprocess.run(['sudo', 'rm', '-rf', '/usr/lib/zookeeper'])
    return


def remove_environement_variable_spark():
    remove_line('/etc/environment', spark_home)
    remove_line('/etc/environment', spark_conf_dir)
    return


def remove_environement_variable_zookeeper():
    remove_line('~/.profile', 'zookeeper')
    return


def remove_line(path_file, string_in_line):
    subprocess.run(['sudo', 'cp', path_file, path_file + '.tmp'])
    with open(path_file + '.tmp') as file_in:
        for line in file_in:
            if string_in_line not in line:
                os.system('echo "' + line + '" | sudo tee -a ' + path_file + ' >> /dev/null 2>&1')

        subprocess.run(['sudo', 'rm', path_file + '.tmp'])
    return


if __name__ == '__main__':
    remove_directory_spark()
    # remove_directory_zookeeper()
    remove_environement_variable_spark()
    # remove_environement_variable_zookeeper()
