#!/usr/bin/env python3

import logging
from threading import Timer
import subprocess
import configparser
import os

components = ['hdfs', 'neo4j', 'rabbitmq', 'spark', 'zookeeper']


def job_server():
    global_check()
    scheduler = Timer(5, job_server)
    scheduler.start()


def global_check():
    logging.info("Start to check all service")
    for service in components:
        config = configparser.ConfigParser()
        config.read("./" + service + "/conf.ini")
        keys = config.sections()
        for key in keys:
            if "Log" not in key:
                hosts = lib_spark.getHostsByKey(config=config, key=key)
                for host in hosts:
                    result = check_function(name_service=service, key_name=key, host=host)

                    if not result:
                        restart(host=host, service=service, key=key)
    logging.info("Finish to check all service")
    return


def check_function(name_service, key_name, host):
    if "zookeeper" in name_service:
        result = check_zookeeper(zookeeper_host=host)
    elif "spark" in name_service:
        if "Master" in key_name:
            result = check_spark_master(spark_master_host=host)
        elif "Slaves" in key_name:
            result = check_spark_worker(spark_worker_host=host)
    elif "rabbitmq" in name_service:
        if "Master" in key_name or "Slaves" in key_name:
            result = check_rabbitmq(rabbitmq_host=host)
    elif "neo4j" in name_service:
        if "Master" in key_name or "Slaves" in key_name:
            result = check_neo4j(neo4j_host=host)
    elif "hdfs" in name_service and "DataNode" in key_name:
        result = check_hdfs(hdfs_host=host)
    return result


# Function who check zookeeper
def check_zookeeper(zookeeper_host):
    zookeeper_host = "149.202.161.176"

    p = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                          'xnet@' + zookeeper_host,
                          'source ~/.profile; zkServer.sh status;'],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if "follower" in p.stdout.read().decode("utf-8").strip(' \n') or "leader" in p.stdout.read().decode(
            "utf-8").strip(' \n'):
        logging.info("On machine " + zookeeper_host + " Zookeeper Running")
        return True
    else:
        logging.warning("On machine " + zookeeper_host + " Zookeeper Not Running")
        return False


# Function who check spark master
def check_spark_master(spark_master_host):
    spark_master_host = "149.202.161.176"

    p = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                          'xnet@' + spark_master_host,
                          'source ~/.profile; spark-daemon status org.apache.spark.deploy.master.Master 1;'],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if "is running" in p.stdout.read().decode("utf-8").strip(' \n'):
        logging.info("On machine " + spark_master_host + " Master Running")
        return True
    else:
        logging.warning("On machine " + spark_master_host + " Master Not Running")
        return False


# Function who check spark worker
def check_spark_worker(spark_worker_host):
    spark_worker_host = "149.202.170.208"

    p1 = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                           'xnet@' + spark_worker_host,
                           'source ~/.profile; spark-daemon status org.apache.spark.deploy.worker.Worker 1;'],
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    p2 = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                           'xnet@' + spark_worker_host,
                           'source ~/.profile; spark-daemon status org.apache.spark.deploy.worker.Worker 1;'],
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if "is running" in p1.stdout.read().decode("utf-8").strip(' \n') and "is running" in p2.stdout.read().decode(
            "utf-8").strip(' \n'):
        logging.info("On machine " + spark_worker_host + " Worker Running")
        return True
    else:
        logging.warning("On machine " + spark_worker_host + " Worker Not Running")
        return False


# Function who check hdfs
def check_hdfs(hdfs_host):
    return True


# Function who check haproxy
def check_haproxy(haproxy_host):
    haproxy_host = "149.202.161.167"

    p = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                          'xnet@' + haproxy_host,
                          'source ~/.profile; sudo service haproxy status;'],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if "Active: active (running)" in p.stdout.read().decode("utf-8").strip(' \n'):
        logging.info("On machine " + haproxy_host + " haproxy Running")
        return True
    else:
        logging.warning("On machine " + haproxy_host + " haproxy Not Running")
        return False


# Function who check rabbitmq
def check_rabbitmq(rabbitmq_host):
    rabbitmq_host = "149.202.161.167"

    p = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                          'xnet@' + rabbitmq_host,
                          'source ~/.profile; sudo rabbitmqctl status;'],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if "rabbitmq_management,\"RabbitMQ Management Console\",\"3.6.6\"" in p.stdout.read().decode("utf-8").strip(
            ' \n'):
        logging.info("On machine " + rabbitmq_host + " rabbitmq Running")
        return True
    else:
        logging.warning("On machine " + rabbitmq_host + " rabbitmq Not Running")
        return False


# Function who check neo4j
def check_neo4j(neo4j_host):
    neo4j_host = "149.202.170.185"

    p = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                          'xnet@' + neo4j_host,
                          'source ~/.profile; sudo /usr/lib/neo4j/neo4j-enterprise-3.0.7/bin/neo4j status;'],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    if "is running" in p.stdout.read().decode("utf-8").strip(' \n'):
        logging.info("On machine " + neo4j_host + " neo4j Running")
        return True
    else:
        logging.warning("On machine " + neo4j_host + " neo4j Not Running")
        return False


def restart(host, service, key):
    logging.info("On machine " + host + " try to start service " + service)
    # call for stop the service
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                    'xnet@' + host,
                    'source ~/.profile; cd SDTD-Mazerunner/script/' + service + '/; python3 stop_' + service + '.py;'],
                   stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    # call for start the service
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '~/.ssh/xnet',
                    'xnet@' + host,
                    'source ~/.profile; cd SDTD-Mazerunner/script/' + service + '/; python3 launch_' + service + '.py;'],
                   stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    result = check_function(name_service=service, key_name=key, host=host)

    if result:
        logging.info("On machine " + host + " restart service " + service + " [success]")
    else:
        logging.info("On machine " + host + " impossible to restart service " + service + "[error]")

    return


if __name__ == '__main__':
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from script.spark import lib_spark

    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")
    scheduler = Timer(5, job_server)
    scheduler.start()
