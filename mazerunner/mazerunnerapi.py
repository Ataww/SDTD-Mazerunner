#!/usr/bin/python3
# coding: utf8

import pika
import logging
import socket
import os
from pywebhdfs.webhdfs import PyWebHdfsClient
from pywebhdfs.errors import PyWebHdfsException, ActiveHostNotFound
from requests.exceptions import ConnectionError
from neo4j.v1 import GraphDatabase, basic_auth
from flask import Flask, jsonify

app = Flask(__name__)
logger = logging.getLogger(__name__)

'''
CONFIGURATIONS VARIABLES
'''

# HDFS configuration
hdfs_namenodes = ["hdfs-1", "hdfs-2"]

# RabbitMQ configuration
rabbitmq_host = "rabbitmq-1"
rabbitmq_port = 5672
rabbitmq_user = "neo4j_user"
rabbitmq_password = "neo4j_user"

# Neo4j configuration
neo4j_username = "neo4j"
neo4j_password = "neo4j_pass"
neo4j_node = "neo4j-3"
neo4j_bolt_port = "7688"


@app.route("/compute_recommendation", defaults={'username': None})
@app.route("/compute_recommendation/<username>")
def compute_recommendation(username):
    if username is None:
        return jsonify("There was no user specified")

    logger.info("Received a computation job for user : "+username)

    # Get data from neo4j
    logger.info("Getting datas from Neo4j...")
    read, records = get_data_from_neo4j(username)
    if read is not True:
        logger.error("There was a problem while trying to connect to Neo4j. Error :"+str(records))
        return jsonify(records)

    # Write it to HDFS in a certain format (csv)
    logger.info("Writing the datas onto HDFS at this location : /jobs_to_do/"+username+".txt ...")
    written, error = write_data_to_hdfs(username, records)
    if written is not True:
        logger.error("There was an error while trying to Write the datas onto HDFS. Error "+str(error))
        return jsonify(error)

    # Notify Spark via RabbitMQ that a subgraph is available
    logger.info("Notifying Spark via RabbitMQ...")
    notified, error = notify_spark_via_rabbitmq(username)
    if notified is not True:
        return jsonify(error)

    # Wait until the computing finish
    logger.info("Wait for the end of calculation...")
    rabbitMQ_consumer = RabbitMQConsumerClient(username)
    rabbitMQ_consumer.start_consuming()

    # Read the job result from HDFS
    logger.info("Reading job result from HDFS...")
    read, result = read_result_from_hdfs(username)
    if read is not True:
        logger.error("There was a problem while reading result from HDFS")
        return result

    # Inject result into neo4j
    logger.info("Injecting result back to neo4j...")
    injected, result = inject_recommendations_into_neo4j(username, result)
    if injected is not True:
        logger.error("There was a problem while injecting result into neo4j")
        return jsonify(result)

    logger.info("Job computation for username "+username+" is over")
    return jsonify("Job computation for username "+username+" is over")


def get_data_from_neo4j(username):
    to_return = {}
    socket.setdefaulttimeout(10)
    try:

        logger.debug("Trying to connect to bolt://"+neo4j_node+":"+neo4j_bolt_port+" ...")
        # Erase known hosts
        # os.system("sudo rm -r /home/xnet/.neo4j/known_hosts")
        driver = GraphDatabase.driver("bolt://"+neo4j_node+":"+neo4j_bolt_port, auth=basic_auth(neo4j_username, neo4j_password))
        session = driver.session()
        logger.debug("Connected to bolt://" + neo4j_node + ":" + neo4j_bolt_port + " ...")
        result = session.run("MATCH (n:Utilisateur)-[r1:AIME]->(t:Titre)<-[r2:AIME]-(n2:Utilisateur)-[r3:AIME]->(t2:Titre) WHERE n.nomUtilisateur = \""+username+"\" AND n2.nomUtilisateur <> \""+username+"\" AND t <> t2 RETURN DISTINCT  n2, type(r3), t2")
        records = ""
        for record in result:
            n2 = record["n2"]
            type = record["type(r3)"]
            t2 = record["t2"]

            # Generate GraphX needed format
            records += n2.get("idUtilisateur")+","+n2.get("nomUtilisateur")+","+type+","+t2.get("idTitre")+"\n"

        session.close()

        return True, records
    except (socket.timeout, socket.gaierror) as e:
        to_return["error"] = "There was a problem while trying to connect to Neo4j"
        to_return["details"] = str(e)
        logger.debug(str(to_return))
        return False, to_return

    return False, None


def inject_recommendations_into_neo4j(username, records):
    to_return = {}
    nb_relationships_created = 0
    socket.setdefaulttimeout(10)
    try:
        logger.debug("Trying to connect to bolt://" + neo4j_node + ":" + neo4j_bolt_port + " ...")
        # os.system("sudo rm -r /home/xnet/.neo4j/known_hosts")
        driver = GraphDatabase.driver("bolt://" + neo4j_node + ":" + neo4j_bolt_port, auth=basic_auth(neo4j_username, neo4j_password))
        session = driver.session()

        for record in records.decode("utf-8").split("\n"):
            values = record.split(",")
            track_id = values[len(values)-1]
            if track_id:
                result = session.run("MATCH (u:Utilisateur {nomUtilisateur:'"+ username +"'}), (t:Titre {idTitre:'"+track_id+"'}) CREATE (u)-[:RECO]->(t)")
                summary = result.consume()
                logger.debug(str(summary.counters.relationships_created)+" recommendation added ("+username+" --RECO--> "+track_id+")")
                nb_relationships_created += summary.counters.relationships_created

        session.close()

        logger.info(str(nb_relationships_created)+" RECO relationships have been created")
        return True, to_return
    except socket.timeout as toe:
        to_return["error"] = "There was a problem while trying to connect to Neo4j"
        to_return["details"] = str(toe)
        logger.debug(str(to_return))
        return False, to_return

    return False, None


def write_data_to_hdfs(username, records):
    global hdfs_namenodes
    to_return = {}
    file_path = "/jobs_to_do/"+username+".txt"
    result_path = "/jobs_done/" + username
    logger.debug("Writing file " + file_path + " to HDFS")
    try:
        logger.debug("Trying to connect to "+hdfs_namenodes[0]+" namenode")
        hdfs_client = PyWebHdfsClient(host=hdfs_namenodes[0], port='50070', user_name='xnet', timeout=100)
        logger.debug("Trying to erase "+file_path)
        logger.debug("Trying to erase "+result_path)
        hdfs_client.delete_file_dir(file_path, recursive=True)
        hdfs_client.delete_file_dir(result_path, recursive=True)
        hdfs_client.create_file(file_path, records.encode("utf-8"))
    except (ConnectionError, PyWebHdfsException) as ce:
        to_return["details_1"] = str(ce)
        logger.debug("Failed connecting to" + hdfs_namenodes[0] + " namenode")
        try:
            logger.debug("Trying to connect to " + hdfs_namenodes[1] + " namenode")
            hdfs_client = PyWebHdfsClient(host=hdfs_namenodes[1], port='50070', user_name='xnet', timeout=100)
            logger.debug("Trying to erase "+file_path)
            logger.debug("Trying to erase "+result_path)
            hdfs_client.delete_file_dir(file_path, recursive=True)
            hdfs_client.delete_file_dir(result_path, recursive=True)
            hdfs_client.create_file(file_path, records.encode("utf-8"))
        except (ConnectionError, PyWebHdfsException) as ce:
            to_return["error"] = "There was a problem while trying to connect to HDFS namenode."
            to_return["details_2"] = str(ce)
            logger.debug(str(to_return))
            return False, to_return

    return True, None


def read_result_from_hdfs(username):
    result = ""
    to_return = {}
    file_path = "/jobs_done/"+username+"/part-00000"
    logger.debug("Reading file " + file_path + " from HDFS")
    try:
        logger.debug("Trying to connect to " + hdfs_namenodes[0] + " namenode")
        hdfs_client = PyWebHdfsClient(host=hdfs_namenodes[0], port='50070', user_name='xnet', timeout=100)
        result = hdfs_client.read_file(file_path)
    except (ActiveHostNotFound,ConnectionError) as e:
        to_return["details_1"] = str(e)
        try:
            logger.debug("Trying to connect to " + hdfs_namenodes[1] + " namenode")
            hdfs_client = PyWebHdfsClient(host=hdfs_namenodes[1], port='50070', user_name='xnet', timeout=100)
            result = hdfs_client.read_file(file_path)
        except (ActiveHostNotFound, ConnectionError) as e2:
            to_return["error"] = "There was a problem while trying to read result from HDFS."
            to_return["details2"] = str(e2)
            logger.debug(str(to_return))
            return False, to_return

    return True, result


def notify_spark_via_rabbitmq(username):
    # Configure RabbitMQ connection
    to_return = {}
    try:
        credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
        sending_connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, '/', credentials))
        rabbitmq_sending_channel = sending_connection.channel()
        rabbitmq_sending_channel.exchange_declare(exchange='jobs_to_do', type='fanout')
        rabbitmq_sending_channel.basic_publish(exchange='jobs_to_do', routing_key='', body=username)
    except Exception as e:
        to_return["error"] = "There was a a problem while notifying Spark via Rabbitmq"
        to_return["details"] = str(e)
        return False, to_return

    return True, None


class RabbitMQConsumerClient():
    def __init__(self, username):
        # Configure RabbitMQ connection
        self.username = username
        self.credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)

        self.receiving_connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, '/', self.credentials))
        self.receiving_channel = self.receiving_connection.channel()
        self.receiving_channel.exchange_declare(exchange='done_jobs', type='fanout')

        result = self.receiving_channel.queue_declare(exclusive=False, queue='done_jobs')
        queue_name = result.method.queue

        self.receiving_channel.queue_bind(exchange='done_jobs', queue=queue_name)
        self.receiving_channel.basic_consume(self.on_new_job_done, queue=queue_name, no_ack=True)

    def start_consuming(self):
        self.receiving_channel.start_consuming()

    def on_new_job_done(self, ch, method, props, body):
        logger.debug("Comparing done job and username : "+body.decode("utf-8")+" == "+self.username+" ? %r" % (body.decode("utf-8") == self.username))
        if(body.decode("utf-8") == self.username):
            self.receiving_channel.stop_consuming()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.ERROR, format="%(asctime)s :: %(levelname)s :: %(message)s")
    logging.getLogger(__name__).setLevel(logging.DEBUG)

    # Run the service
    app.run(host='0.0.0.0', threaded=True)
