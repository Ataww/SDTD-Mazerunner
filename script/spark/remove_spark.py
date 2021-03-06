#!/usr/bin/env python3

import subprocess
import os
import logging


def remove_directory_spark():
    logging.info("Remove All files installed")
    os.system('stop-master >> /dev/null 2>&1')
    os.system('stop-slave >> /dev/null 2>&1')
    subprocess.run(['sudo', 'rm', '-rf', '/usr/lib/spark'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'rm', '/sbin/stop-master'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'rm', '/sbin/stop-slave'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'rm', '/sbin/start-master'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'rm', '/sbin/start-slave'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'rm', '/bin/spark-submit'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'rm', '/sbin/spark-daemon'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return


def remove_environement_variable_spark():
    logging.info("Remove All variable of environment of spark")
    remove_line('/etc/environment', 'SPARK')
    return


def remove_line(path_file, string_in_line):
    subprocess.run(['sudo', 'cp', path_file, path_file + '.tmp'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'rm', path_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['sudo', 'touch', path_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(path_file + '.tmp', 'r') as file_in:
        for line in file_in:
            if string_in_line not in line:
                line = line.strip(' \n')
                os.system('echo ' + line + ' | sudo tee -a ' + path_file + ' >> /dev/null 2>&1')

    subprocess.run(['sudo', 'rm', path_file + '.tmp'])
    return


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

    remove_directory_spark()
    remove_environement_variable_spark()
