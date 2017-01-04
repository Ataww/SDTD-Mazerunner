#! /usr/bin/env python

from flask import Flask
app = Flask(__name__)

@app.route("/compute_recommendation", defaults={'username': None})
@app.route("/compute_recommendation/<username>")
def compute_recommendation(username):
    if username is None:
        print "No user specified"
    else:
        print "Computing recommendation for" + username

    # Get required graph from neo4j

    # Write it to HDFS

    # Notify Spark via RabbitMQ that a subgraph is available

    # Wait until the computing finish

    # Inject the computed result into neo4j

if __name__ == "__main__":
    app.run()