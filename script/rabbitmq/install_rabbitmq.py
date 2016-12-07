#!/usr/bin/env python3

import subprocess, os, sys, logging, socket, configparser

def install_server() :
    logging.info('Add RabbitMQ as source for apt-get')
    source = subprocess.Popen(('echo',"deb http://www.rabbitmq.com/debian/ testing main"), stdout=subprocess.PIPE)
    apt = subprocess.check_output(('sudo', 'tee', '/etc/apt/sources.list.d/rabbitmq.list'), stdin=source.stdout)
    source.wait()

    logging.info('Install rabbitMQ Server')
    subprocess.run(['sudo', 'apt-get', 'update'])
    subprocess.run(['sudo', 'apt-get', 'install', '-y', 'rabbitmq-server'])

    return

def configure_user() :
    logging.info('Delete default user guest')
    subprocess.run(['sudo', 'rabbitmqctl', 'delete_user', 'guest'])
    # Create
    logging.info('Add two user with full access on vhost / : neao4j_user and spark_user')
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
    subprocess.run(['sudo','scp', '-i', '/home/xnet/.ssh/xnet', 'xnet@' + master + ':/tmp/.erlang.cookie', '/tmp/'])
    subprocess.run(['sudo', 'cp', '/tmp/.erlang.cookie', '/var/lib/rabbitmq/'])
    subprocess.run(['sudo', 'service', 'rabbitmq-server', 'start'])
    return

def configure_logger(debug):
    logging.basicConfig(filename="install_rabbitmq.log", format="%(asctime)s :: %(levelname)s :: %(message)s")
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
    masterHost = config.get("Master", "host")
    slaveHosts = config.get("Slaves", 'hosts').split(',')
    DEBUG = config.get("Log", "debug")

    # Configure logger
    configure_logger(DEBUG)

    hostname = socket.gethostname()
    logging.info('Going to install RabbitMQ on' + hostname)

    #Install
    install_server()
    if hostname == masterHost :
        configure_user()
        expose_erlang_cookie()
        configure_replication()
    else:
        take_erlang_cookie(masterHost)
        join_cluster(masterHost)

    logging.info('RabbitMQ installation done')

    return

# INSTALLATION
install_rabbitmq()
