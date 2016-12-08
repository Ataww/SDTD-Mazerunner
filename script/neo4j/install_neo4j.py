#!/usr/bin/env python3

import os
import logging
import subprocess
from os.path import exists

neo4j_version = 'neo4j-enterprise-3.0.7-unix'

# Function to install Neo4j
def install_neo4j():
    if not exists("/usr/lib/neo4j/neo4j-enterprise-3.0.7"):
        logging.info("Downloading Neo4j ...")
        out = subprocess.run(['sudo', 'wget', '-q', 'https://neo4j.com/artifact.php?name='+neo4j_version+'.tar.gz'], check=True)
        if out.returncode == 0:
            logging.info("Neo4j downloaded successfully [success]")
        else:
            logging.error("Neo4j downloaded echec [error]")


        logging.info("Installation of Neo4J ...")
        subprocess.run(['sudo', 'rm', '-rf', '/usr/lib/neo4j'])
        subprocess.run(['sudo', 'mkdir', '/usr/lib/neo4j'])
        out = subprocess.run(['sudo', 'tar', '-xzf', 'artifact.php?name='+neo4j_version+'.tar.gz', '-C', '/usr/lib/neo4j'], check=True)
        if out.returncode == 0:
            logging.info("Neo4j unpacked [success]")
        else:
            logging.error("Neo4j unpacked with error [error]")
        subprocess.run(["rm", 'artifact.php?name='+neo4j_version+'.tar.gz'])
        logging.info("Neo4j installation is done")
        return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    install_neo4j()
