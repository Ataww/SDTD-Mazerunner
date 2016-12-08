#!/usr/bin/env python3

import os
import logging
import subprocess

neo4j_version = 'neo4j-enterprise-3.0.7'

# Function to install Neo4j
def launch_neo4j():
    logging.info("Launching Neo4j ...")
    subprocess.Popen('ulimit -n 40000', shell=True)
    subprocess.run(['sudo', '/usr/lib/neo4j/'+neo4j_version+'/bin/neo4j', 'start'])
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    launch_neo4j()
