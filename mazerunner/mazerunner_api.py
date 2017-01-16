#!/usr/bin/python3
# coding: utf8

import pika
import json
import logging
from pywebhdfs.webhdfs import PyWebHdfsClient
from pywebhdfs.errors import PyWebHdfsException
from requests.exceptions import ConnectionError, ActiveHostNotFound
from neo4j.v1 import GraphDatabase, basic_auth
from flask import Flask, jsonify
app = Flask(__name__)

hdfs_namenodes = ["hdfs-1", "hdfs-2"]

# RabbitMQ
rabbitmq_host = "rabbitmq-1"
rabbitmq_port = 5672

@app.route("/compute_recommendation", defaults={'username': None})
@app.route("/compute_recommendation/<username>")
def compute_recommendation(username):
    if username is None:
        return jsonify("There was no user specified")

    logging.info("Received a computation job for user : "+username)

    # Get required graph from neo4j
    logging.info("Getting datas from Neo4j...")

    # Configure neo4j connection
    records = get_data_from_neo4j(username)

    # Write it to HDFS
    logging.info("Writing the datas onto HDFS at this location : /jobs_to_do/"+username+".txt")
    written, error = write_data_to_hdfs(username, records)

    if written is not True:
        return error

    # Notify Spark via RabbitMQ that a subgraph is available
    logging.info("Notifying Spark via RabbitMQ...")
    notify_spark_via_rabbitmq(username)

    # Wait until the computing finish
    logging.info("Wait for the end of calculation...")
    rabbitMQ_consumer = RabbitMQConsumerClient(username)
    rabbitMQ_consumer.start_consuming()

    # Inject the computed result into neo4j
    logging.info("Reading computing result...")
    result = read_result_from_hdfs(username)

    return jsonify("Job computation for username "+username+" is over")

def get_data_from_neo4j(username):
    neo4j_client = GraphDatabase.driver("bolt://149.202.170.185:7687", auth=basic_auth("neo4j", "neo4j_pass")).session()
    result = neo4j_client.run("MATCH (n:Utilisateur)-[r1:AIME]->(t:Titre)<-[r2:AIME]-(n2:Utilisateur)-[r3:AIME]->(t2:Titre) WHERE n.nomUtilisateur = \""+username+"\" AND n2.nomUtilisateur <> \""+username+"\" AND t <> t2 RETURN DISTINCT  n2, type(r3), t2")
    records = "n2,type(r3),t2\n"
    for record in result:
        n2 = record["n2"]
        type = record["type(r3)"]
        t2 = record["t2"]

        n2_str = "{\"nomUtilisateur\":\""+n2.get("nomUtilisateur")+"\",\"idUtilisateur\":\""+n2.get("idUtilisateur")+"\"}"
        t2_str = "{\"idTitre\":\""+t2.get("idTitre")+"\",\"artiste\":\""+t2.get("artiste")+"\",\"nomChanson\":\""+t2.get("nomChanson")+"\"}"

        records += n2_str+","+type+","+t2_str+"\n"

    return records

def write_data_to_hdfs(username, records):
    # Configure WebHDFS connection
    global hdfs_namenodes
    try:
        to_return = {}
        try:
            logging.info("Trying to connect to "+hdfs_namenodes[0]+" namenode")
            hdfs_client = PyWebHdfsClient(host=hdfs_namenodes[0], port='50070', user_name='xnet', timeout=100)
            hdfs_client.create_file("/jobs_to_do/"+username+".txt", records.encode("utf-8"))
        except ConnectionError as ce:
            to_return["details_1"] = str(ce)
            try:
                logging.info("Trying to connect to " + hdfs_namenodes[1] + " namenode")
                hdfs_client = PyWebHdfsClient(host=hdfs_namenodes[1], port='50070', user_name='xnet', timeout=100)
                hdfs_client.create_file("/jobs_to_do/" + username + ".txt", records.encode("utf-8"))
            except ConnectionError as ce:
                to_return["error"] = "There was a problem while trying to connect to HDFS namenode."
                to_return["details_2"] = str(ce)
                logging.info(json.dumps(to_return))
                return False, jsonify(to_return)

    except PyWebHdfsException as e:
        to_return = {}
        to_return["error"] = "There was a problem while trying to write neo4j request data into HDFS."
        to_return["details"] = json.loads(e.msg.decode("utf-8"))
        logging.info(json.dumps(to_return))
        return False ,jsonify(to_return)

    return True, None

def read_result_from_hdfs(username):
    # Configure WebHDFS connection
    hdfs_client = PyWebHdfsClient(host=hdfs_namenodes[0], port='50070', user_name='xnet', timeout=100)
    result = hdfs_client.read_file("/jobs_to_do/" + username + ".txt")
    return result

def notify_spark_via_rabbitmq(username):
    # Configure RabbitMQ connection
    credentials = pika.PlainCredentials("neo4j_user", "neo4j_user")
    sending_connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, '/', credentials))
    rabbitmq_sending_channel = sending_connection.channel()
    rabbitmq_sending_channel.exchange_declare(exchange='jobs_to_do', type='fanout')
    rabbitmq_sending_channel.basic_publish(exchange='jobs_to_do', routing_key='', body=username)

class RabbitMQConsumerClient():
    def __init__(self, username):
        # Configure RabbitMQ connection
        self.username = username
        self.credentials = pika.PlainCredentials("neo4j_user", "neo4j_user")

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
        logging.info(body.decode("utf-8")+" == "+self.username+" ? %r" % (body.decode("utf-8") == self.username))
        if(body.decode("utf-8") == self.username):
            self.receiving_channel.stop_consuming()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

    # Run the service
    app.run(threaded=True)