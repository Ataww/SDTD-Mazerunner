#!/usr/bin/env python3

import os
import logging
import subprocess

neo4j_version = 'neo4j-enterprise-3.0.7-unix'

# Function to install Neo4j
def install_neo4j():
    logging.info(" Downloading Neo4j ...")
    out = subprocess.run(['sudo', 'wget', '-q', 'https://neo4j.com/artifact.php?name='+neo4j_version+'.tar.gz'], check=True)
    if out.returncode == 0:
        logging.info(" Neo4j downloaded successfully")

    logging.info(" Installation of Neo4J ...")
    subprocess.run(['sudo', 'rm', '-rf', '/usr/lib/neo4j'])
    subprocess.run(['sudo', 'mkdir', '/usr/lib/neo4j'])
    out = subprocess.run(['sudo', 'tar', '-xzvf', 'artifact.php?name='+neo4j_version+'.tar.gz', '-C', '/usr/lib/neo4j'], check=True)
    if out.returncode == 0:
        logging.info("Neo4j unpacked")
    subprocess.run(["rm", 'artifact.php?name='+neo4j_version+'.tar.gz'])
    return

install_neo4j()
