#!/usr/bin/env python3

import subprocess, os, sys, logging, socket, configparser
from os.path import exists

def install_server() :
    if not exists("/usr/lib/rabbitmq/bin/rabbitmq-server"):
        logging.info('Add RabbitMQ as source for apt-get')
        source = subprocess.Popen(('echo',"deb http://www.rabbitmq.com/debian/ testing main"), stdout=subprocess.PIPE)
        apt = subprocess.check_output(('sudo', 'tee', '/etc/apt/sources.list.d/rabbitmq.list'), stdin=source.stdout)
        source.wait()

        logging.info('Install rabbitMQ Server')
        os.system("sudo apt-get update >> /dev/null 2>&1")
        out = os.system('sudo apt-get -qq -y --allow-unauthenticated install rabbitmq-server >> /dev/null 2>&1')
        if out == 0:
           logging.info("rabbitmq-server installed [success]")
        else:
           logging.error("rabbitmq-server installation failed [error]")

    return

def enable_management_UI() :
    logging.info('Enable WEB UI')
    subprocess.run(['sudo', 'rabbitmq-plugins', 'enable', 'rabbitmq_management'])
    return

def configure_user() :
    logging.info('Delete default user guest')
    subprocess.run(['sudo', 'rabbitmqctl', 'delete_user', 'guest'])
    # Create
    logging.info('Add two user with full access on vhost / : neo4j_user and spark_user')
    subprocess.run(['sudo', 'rabbitmqctl', 'add_user', 'neo4j_user', 'neo4j_user'])
    subprocess.run(['sudo', 'rabbitmqctl', 'add_user', 'spark_user', 'spark_user'])
    # Add tags
    logging.info('Add tags administrator')
    subprocess.run(['sudo', 'rabbitmqctl', 'set_user_tags', 'neo4j_user', 'administrator'])
    subprocess.run(['sudo', 'rabbitmqctl', 'set_user_tags', 'spark_user', 'administrator'])
    # Set permissions on vhost /
    logging.info('Give all permission on vhost /')
    subprocess.run(['sudo', 'rabbitmqctl', 'set_permissions', '-p', '/', 'neo4j_user', '.*', '.*', '.*'])
    subprocess.run(['sudo', 'rabbitmqctl', 'set_permissions', '-p', '/', 'spark_user', '.*', '.*', '.*'])
    return

def join_cluster(master):
    logging.info('Going to join cluster with ' + master)
    subprocess.run(['sudo', 'rabbitmqctl', 'stop_app'])
    subprocess.run(['sudo', 'rabbitmqctl', 'join_cluster', 'rabbit@'+master])
    subprocess.run(['sudo', 'rabbitmqctl', 'start_app'])
    return

def configure_replication() :
    logging.info('Configuring queues replication')
    # Queues are replicated on each nodes
    subprocess.run(['sudo', 'rabbitmqctl', 'set_policy', 'ha-all', '"[^=]*"','{"ha-mode":"all", "ha-sync-mode":"automatic"}'])
    return

def expose_erlang_cookie() :
    logging.info('Expose erlang cookie in /tmp for slaves')
    subprocess.run(['sudo' ,'cp', '/var/lib/rabbitmq/.erlang.cookie', '/tmp'])
    subprocess.run(['sudo', 'chmod', 'o+r', '/tmp/.erlang.cookie'])
    return

def take_erlang_cookie(master) :
    logging.info('Take erlang cookie from ' + master)
    # TODO do not use directly username xnet
    subprocess.run(['sudo', 'service', 'rabbitmq-server', 'stop'])
    subprocess.run(['sudo','scp', '-o','StrictHostKeyChecking=no', '-i', '/home/xnet/.ssh/xnet', 'xnet@' + master + ':/tmp/.erlang.cookie', '/tmp/'])
    subprocess.run(['sudo', 'cp', '/tmp/.erlang.cookie', '/var/lib/rabbitmq/'])
    subprocess.run(['sudo', 'service', 'rabbitmq-server', 'start'])
    return

def install_haproxy():
    subprocess.run(['sudo','apt-get','-qq','-y','install','haproxy'])
    subprocess.run(['mkdir','-p','/etc/haproxy'])
    subprocess.run(['sudo','cp','/home/xnet/SDTD-Mazerunner/script/rabbitmq/conf/haproxy.cfg','/etc/haproxy/'])
    subprocess.run(['sudo', 'service', 'haproxy', 'restart'])
    return

def configure_logger(debug):
    logging.basicConfig(format="%(asctime)s :: %(levelname)s :: %(message)s")
    logger = logging.getLogger()
    if debug == 'True':
        logger.setLevel(logging.DEBUG)
    else :
        logger.setLevel(logging.INFO)
    return

def install_rabbitmq():
    # Read configuration
    config = configparser.ConfigParser()
    config.read("conf.ini")
    masterHost = getHostsByKey(config, "Master")
    slaveHosts = config.get("Slaves", 'hosts').split(',')
    DEBUG = config.get("Log", "debug")

    # Configure logger
    configure_logger(DEBUG)

    hostname = get_hostname()

    if not exists("/usr/lib/rabbitmq/bin/rabbitmq-server"):
        logging.info('Going to install RabbitMQ on ' + hostname)

        #Install
        install_server()
        enable_management_UI()
        if hostname == masterHost[0]:
            install_haproxy()
            configure_user()
            expose_erlang_cookie()
            configure_replication()
        else:
            take_erlang_cookie(masterHost[0])
            join_cluster(masterHost[0])

        logging.info('RabbitMQ installation done')

    return

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

# Recover all ip for one component. Return format ip
def getHostsByKey(config, key):
    hosts = config.get(key, "hosts").split(',')
    index = 0
    for host in hosts:
        hosts[index] = host.strip(' \n')
        index += 1
    return hosts

# Copy monit script on hostname
def copy_monit_file(monitFile, hostname):
    logging.info('Copying monit config files ' + monitFile + ' on host ' + hostname)
    subprocess.run(['sudo', 'cp', 'etc/monit/' + monitFile, '/etc/monit/conf.d/'])
    return

# Deploy monit conf script
def conf_monit():
    logging.info('Add monit config file')
    hostname = socket.gethostname()
    config = configparser.ConfigParser()
    config.read('conf.ini')

    masterMonitHosts = config.get("Master", 'hosts').split(',')
    slavesMonitHosts = config.get("Slaves", 'hosts').split(',')
    masterMonitFile = config.get("Master", 'monitFile').split(',')
    slavesMonitFile = config.get("Slaves", 'monitFile').split(',')

    if not exists('/etc/monit'):
        logging.error('monit is not installed')
    else:
        for host in masterMonitHosts:
            if hostname == host:
                for monitFile in masterMonitFile:
                    copy_monit_file(monitFile, hostname)
        for host in slavesMonitHosts:
            if hostname == host:
                for monitFile in slavesMonitFile:
                    copy_monit_file(monitFile, hostname)
    subprocess.run(['sudo', 'monit', 'reload'])

# INSTALLATION
if __name__ == '__main__':
    install_rabbitmq()
    conf_monit()
