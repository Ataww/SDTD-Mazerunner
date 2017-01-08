#! /usr/bin/env python
import pika
from pywebhdfs.webhdfs import PyWebHdfsClient
from neo4j.v1 import GraphDatabase, basic_auth
from flask import Flask
app = Flask(__name__)

# Neo4j
neo4j_client = None

# HDFS
hdfs_client = None
namenode_server = "149.202.161.176"

# RabbitMQ
rabbitmq_host = "rabbitmq-1"
rabbitmq_port = 5672
rabbitmq_sending_channel = None
rabbitmq_receiving_channel = None

@app.route("/compute_recommendation", defaults={'username': None})
@app.route("/compute_recommendation/<username>")
def compute_recommendation(username):
    if username is None:
        return "There was no user specified"


    # Get required graph from neo4j
    json = "{name:\"toto\"}";

    # Write it to HDFS
    hdfs_client.create_file("/jobs_to_do/"+username+".json", json)

    # Notify Spark via RabbitMQ that a subgraph is available
    rabbitmq_sending_channel.basic_publish(exchange='jobs_to_do', routing_key='', body=username)

    # Wait until the computing finish


    # Inject the computed result into neo4j
    result = hdfs_client.read_file("/results/"+username+".json")

    return "Computation's over"


if __name__ == "__main__":

    # Configure neo4j connection
    # neo4j_client = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "neo4j")).session()

    # Configure WebHDFS connection
    hdfs_client = PyWebHdfsClient(host=namenode_server, port='50070', user_name='xnet')

    # Configure RabbitMQ connection
    credentials = pika.PlainCredentials("neo4j_user", "neo4j_user")
    sending_connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, '/', credentials))
    receiving_connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host, rabbitmq_port, '/', credentials))
    rabbitmq_sending_channel = sending_connection.channel()
    rabbitmq_receiving_channel = receiving_connection.channel()
    rabbitmq_sending_channel.exchange_declare(exchange='jobs_to_do', type='fanout')


    # Run the service
    app.run()