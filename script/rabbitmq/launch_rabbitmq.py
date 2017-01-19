#!/usr/bin/env python3
import subprocess, logging, configparser, socket


def launch_rabbitmq():
    subprocess.run(['sudo', 'systemctl', 'start', 'rabbitmq-server'])
    return


def launch_haproxy():
    subprocess.run(['sudo', 'service', 'haproxy', 'start'])
    return


# Recover all ip for one component. Return format ip
def getHostsByKey(config, key):
    hosts = config.get(key, "hosts").split(',')
    index = 0
    for host in hosts:
        hosts[index] = host.strip(' \n')
        index += 1
    return hosts


# Permit to know the hostname
def get_hostname():
    config = configparser.ConfigParser()
    config.read("conf.ini")
    hosts = getHostsByKey(config, "Master")
    hostname = socket.gethostname()

    for host in hosts:
        if host in hostname:
            return host

    hosts = getHostsByKey(config, "Slaves")
    for host in hosts:
        if host in hostname:
            return host

    return hostname

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")
    config = configparser.ConfigParser()
    config.read("conf.ini")
    masterHost = getHostsByKey(config, "Master")
    hostname = get_hostname()
    if hostname == masterHost[0]:
        launch_haproxy()
    launch_rabbitmq()
