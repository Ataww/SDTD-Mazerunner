#!/usr/bin/env python3

import logging
from threading import Timer
import subprocess
import configparser
import os
import smtplib

components = ['hdfs', 'neo4j', 'rabbitmq', 'spark', 'zookeeper']


def job_server():
    global_check()
    scheduler = Timer(60, job_server)
    scheduler.start()


def global_check():
    logging.info("Start to check all service")
    for service in components:
        config = configparser.ConfigParser()
        config.read("/home/xnet/SDTD-Mazerunner/script/" + service + "/conf.ini")
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
    result = True
    if "zookeeper" in name_service and check_host(host):
        result = check_zookeeper(zookeeper_host=host)
    elif "spark" in name_service:
        if "Master" in key_name and check_host(host):
            result = check_spark_master(spark_master_host=host)
        elif "Slaves" in key_name and check_host(host):
            result = check_spark_worker(spark_worker_host=host)
    elif "rabbitmq" in name_service and check_host(host):
        if ("Master" in key_name or "Slaves" in key_name) and check_host(host):
            result = check_rabbitmq(rabbitmq_host=host)
    elif "neo4j" in name_service:
        if ("Master" in key_name or "Slaves" in key_name) and check_host(host):
            result = check_neo4j(neo4j_host=host)
    elif "hdfs" in name_service and "DataNode" in key_name and check_host(host):
        result = check_hdfs(hdfs_host=host)
    return result


# Function who check zookeeper
def check_zookeeper(zookeeper_host):
    p = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '/home/xnet/.ssh/xnet',
                          'xnet@' + zookeeper_host,
                          'source /home/xnet/.profile; zkServer.sh status;'],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p.stdout.read().decode("utf-8").strip(' \n')
    if "follower" in out or "leader" in out:
        logging.info("On machine " + zookeeper_host + " Zookeeper Running")
        return True
    else:
        logging.warning("On machine " + zookeeper_host + " Zookeeper Not Running")
        return False


# Function who check spark master
def check_spark_master(spark_master_host):
    p = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '/home/xnet/.ssh/xnet',
                          'xnet@' + spark_master_host,
                          'source /home/xnet/.profile; spark-daemon status org.apache.spark.deploy.master.Master 1;'],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if "is running" in p.stdout.read().decode("utf-8").strip(' \n'):
        logging.info("On machine " + spark_master_host + " Master Running")
        return True
    else:
        logging.warning("On machine " + spark_master_host + " Master Not Running")
        return False


# Function who check spark worker
def check_spark_worker(spark_worker_host):
    p1 = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '/home/xnet/.ssh/xnet',
                           'xnet@' + spark_worker_host,
                           'source /home/xnet/.profile; spark-daemon status org.apache.spark.deploy.worker.Worker 1;'],
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    p2 = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '/home/xnet/.ssh/xnet',
                           'xnet@' + spark_worker_host,
                           'source /home/xnet/.profile; spark-daemon status org.apache.spark.deploy.worker.Worker 2;'],
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
    p = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '/home/xnet/.ssh/xnet',
                          'xnet@' + hdfs_host,
                          'source /home/xnet/.profile; sudo jps;'],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    out = p.stdout.read().decode("utf-8").strip(' \n')

    if 'hdfs-1' in hdfs_host:
        if "JournalNode" in out and "NameNode" in out:
            logging.info("On machine " + hdfs_host + " hdfs Running")
            return True
        else:
            logging.warning("On machine " + hdfs_host + " hdfs Not Running")
            return False
    elif 'hdfs-2' in hdfs_host:
        if "JournalNode" in out and "NameNode" in out and "DataNode" in out:
            logging.info("On machine " + hdfs_host + " hdfs Running")
            return True
        else:
            logging.warning("On machine " + hdfs_host + " hdfs Not Running")
            return False
    elif 'hdfs-3' in hdfs_host:
        if "JournalNode" in out and "DataNode" in out:
            logging.info("On machine " + hdfs_host + " hdfs Running")
            return True
        else:
            logging.warning("On machine " + hdfs_host + " hdfs Not Running")
            return False
    else:
        return True


# Function who check haproxy
def check_haproxy(haproxy_host):
    p = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '/home/xnet/.ssh/xnet',
                          'xnet@' + haproxy_host,
                          'source /home/xnet/.profile; sudo service haproxy status;'],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if "Active: active (running)" in p.stdout.read().decode("utf-8").strip(' \n'):
        logging.info("On machine " + haproxy_host + " haproxy Running")
        return True
    else:
        logging.warning("On machine " + haproxy_host + " haproxy Not Running")
        return False


# Function who check rabbitmq
def check_rabbitmq(rabbitmq_host):
    p = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '/home/xnet/.ssh/xnet',
                          'xnet@' + rabbitmq_host,
                          'source /home/xnet/.profile; sudo rabbitmqctl status;'],
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
    p = subprocess.Popen(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '/home/xnet/.ssh/xnet',
                          'xnet@' + neo4j_host,
                          'source /home/xnet/.profile; sudo /usr/lib/neo4j/neo4j-enterprise-3.0.7/bin/neo4j status;'],
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
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '/home/xnet/.ssh/xnet',
                    'xnet@' + host,
                    'source /home/xnet/.profile; cd SDTD-Mazerunner/script/' + service + '/; python3 stop_' + service + '.py;'],
                   stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    # call for start the service
    subprocess.run(['ssh', '-o', 'StrictHostKeyChecking=no', '-i', '/home/xnet/.ssh/xnet',
                    'xnet@' + host,
                    'source /home/xnet/.profile; cd SDTD-Mazerunner/script/' + service + '/; python3 launch_' + service + '.py;'],
                   stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    result = check_function(name_service=service, key_name=key, host=host)

    if result:
        logging.info("On machine " + host + " restart service " + service + " [success]")
        send_mail("Service " + service + " on machine " + host + "was stopped but was restart with success")
    else:
        logging.info("On machine " + host + " impossible to restart service " + service + "[error]")
        send_mail("Service " + service + " on machine " + host + "was stopped and could not be restart ")

    return

def check_host(host):
    if lib.hostIsUp(host):
        return True

    send_mail("machine " + host + " is not accessible [error]")
    logging.error("machine " + host + " is not accessible [error]")
    return False

def send_mail(msg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("sdtdmazerunner@gmail.com", "Lgd-nf3-tTP-6yQ")

    server.sendmail("sdtdmazerunner@gmail.com", "sdtdmazerunner@gmail.com", msg)
    server.quit()
    return


if __name__ == '__main__':
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from spark import lib_spark
    from lib import lib

    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")
    scheduler = Timer(5, job_server)
    scheduler.start()
