#!/usr/bin/env python3

import os
import logging
import subprocess

neo4j_version = 'neo4j-enterprise-3.0.7'

# Function to install Neo4j
def stop_neo4j():
    logging.info(" Stopping Neo4j ...")
    subprocess.run(['sudo', '/usr/lib/neo4j/'+neo4j_version+'/bin/neo4j', 'stop'])
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    stop_neo4j()
