#!/usr/bin/python3
# coding: utf8

import pika
import json
import logging
from pywebhdfs.webhdfs import PyWebHdfsClient
from pywebhdfs.errors import PyWebHdfsException
from neo4j.v1 import GraphDatabase, basic_auth
from flask import Flask, jsonify
app = Flask(__name__)

# Neo4j
neo4j_client = None

# HDFS
hdfs_client = None
namenode_server = "hdfs-2"

# RabbitMQ
rabbitmq_host = "rabbitmq-1"
rabbitmq_port = 5672
rabbitmq_sending_channel = None
rabbitmq_receiving_channel = None

@app.route("/compute_recommendation", defaults={'username': None})
@app.route("/compute_recommendation/<username>")
def compute_recommendation(username):
    if username is None:
        return jsonify("There was no user specified")

    logging.info("Received a computation job for user : "+username)

    # Get required graph from neo4j
    logging.info("Getting datas from Neo4j...")
    result = neo4j_client.run("MATCH (n) RETURN n")
    records = ""
    for record in result:
        records += str(record)+"\n"

    logging.info("Retrieved datas :\n")
    logging.info(records)

    # Write it to HDFS
    logging.info("Writing the datas onto HDFS at this location : /jobs_to_do/"+username+".txt")
    try:
        hdfs_client.create_file("/jobs_to_do/"+username+".txt", records.encode("utf-8"))
    except PyWebHdfsException as e:
        to_return = {}
        to_return["error"] = "There was a problem while trying to write neo4j request data into HDFS."
        to_return["details"] = json.loads(e.msg.decode("utf-8"))
        logging.info(json.dumps(to_return))
        return jsonify(to_return)

    # Notify Spark via RabbitMQ that a subgraph is available
    logging.info("Notifying Spark via RabbitMQ...")
    rabbitmq_sending_channel.basic_publish(exchange='jobs_to_do', routing_key='', body=username)

    # Wait until the computing finish
    rabbitmq_receiving_channel.start_consuming()

    # Inject the computed result into neo4j
    logging.info("Reading computing result...")
    result = hdfs_client.read_file("/jobs_to_do/"+username+".txt")

    print(result)

    return jsonify("Job computation for username "+username+" is over")

def on_new_job_done(ch, method, properties, body):
    print(" [x] Received %r" % body)
    rabbitmq_receiving_channel.stop_consuming()

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s :: %(levelname)s :: %(message)s")

    # Configure neo4j connection
    neo4j_client = GraphDatabase.driver("bolt://149.202.170.185:7687", auth=basic_auth("neo4j", "neo4j_pass")).session()

    # Configure WebHDFS connection
    hdfs_client = PyWebHdfsClient(host=namenode_server, port='50070', user_name='xnet', timeout=10000)

    # Configure RabbitMQ connection
    credentials = pika.PlainCredentials("neo4j_user", "neo4j_user")
    # connections
    sending_connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, '/', credentials))
    receiving_connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, '/', credentials))
    # channels
    rabbitmq_sending_channel = sending_connection.channel()
    rabbitmq_receiving_channel = receiving_connection.channel()
    # exchanges
    rabbitmq_sending_channel.exchange_declare(exchange='jobs_to_do', type='fanout')
    rabbitmq_receiving_channel.exchange_declare(exchange='done_jobs', type='fanout')
    result = rabbitmq_receiving_channel.queue_declare(exclusive=False, queue='done_jobs')
    queue_name = result.method.queue
    rabbitmq_receiving_channel.queue_bind(exchange='done_jobs', queue=queue_name)
    rabbitmq_receiving_channel.basic_consume(on_new_job_done,queue=queue_name,no_ack=True)

    # Run the service
    app.run()