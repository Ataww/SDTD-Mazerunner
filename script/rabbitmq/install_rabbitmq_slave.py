#!/usr/bin/env python3

import subprocess, os, sys, logging, socket


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
    # Add Atgs
    subprocess.run(['sudo', 'rabbitmqctl', 'set_user_tags', 'neo4j_user', 'administrator'])
    subprocess.run(['sudo', 'rabbitmqctl', 'set_user_tags', 'spark_user', 'administrator'])
    # Set permissions on vhost /
    subprocess.run(['sudo', 'rabbitmqctl', 'set_permissions', '-p', '/', 'neo4j_user', '.*', '.*', '.*'])
    subprocess.run(['sudo', 'rabbitmqctl', 'set_permissions', '-p', '/', 'spark_user', '.*', '.*', '.*'])
    return

def configure_cluster():
    logging.info('Configuring machine for clustering')
    f = open('/etc/hostname', 'w')
    f.write('rabbitmq-2\n149.202.161.167 rabbitmq-1')
    f.close()
    subprocess.run(['sudo', 'hostname', 'rabbitmq-2'])
    subprocess.run(['sudo', 'rabbitmqctl', 'stop_app'])
    subprocess.run(['sudo', 'rabbitmqctl', 'reset'])
    subprocess.run(['sudo', 'rabbitmqctl', 'join_cluster', 'rabbit@rabbitmq-1'])
    subprocess.run(['sudo', 'rabbitmqctl', 'start_app'])
    return

def install_rabbitmq():
    logging.info('Going to install RabbitMQ on' + socket.gethostname())
    install_server()
    configure_user()
    configure_cluster()
    logging.info('RabbitMQ installation done');
    return

install_rabbitmq()
