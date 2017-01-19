#!/usr/bin/env python3

import subprocess
import os
import logging


def remove_directory_zookeeper():
    logging.info("Remove All files installed")
    os.system('zkServer.sh stop >> /dev/null 2>&1')
    subprocess.run(['sudo', 'rm', '-rf', '/usr/lib/zookeeper'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return


def remove_environement_variable_zookeeper():
    logging.info("Remove All variable of environment of spark")
    path_file = '/etc/environment'
    subprocess.run(['sudo', 'cp', path_file, path_file + '.tmp'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'rm', path_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'touch', path_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(path_file + '.tmp', 'r') as file_in:
        for line in file_in:
            if 'zookeeper' not in line:
                line = line.strip(' \n')
                os.system('echo ' + line + ' | sudo tee -a ' + path_file + ' >> /dev/null 2>&1')

    subprocess.run(['sudo', 'rm', path_file + '.tmp'])
    return


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")
    remove_directory_zookeeper()
    remove_environement_variable_zookeeper()
