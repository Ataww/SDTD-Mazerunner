#!/usr/bin/env python3

import logging
import subprocess
import socket
from os.path import exists

neo4j_version = 'neo4j-enterprise-3.0.7-unix'
neo4j_path = 'neo4j-enterprise-3.0.7'


# Function to install Neo4j
def install_neo4j():
    if not exists("/usr/lib/neo4j/neo4j-enterprise-3.0.7"):
        logging.info("Downloading Neo4j ...")
        out = subprocess.run(['sudo', 'wget', '-q', 'https://neo4j.com/artifact.php?name=' + neo4j_version + '.tar.gz'],
                             check=True)
        if out.returncode == 0:
            logging.info("Neo4j downloaded successfully [success]")
        else:
            logging.error("Neo4j downloaded echec [error]")

        logging.info("Installation of Neo4J ...")
        subprocess.run(['sudo', 'rm', '-rf', '/usr/lib/neo4j'])
        subprocess.run(['sudo', 'mkdir', '/usr/lib/neo4j'])
        out = subprocess.run(
            ['sudo', 'tar', '-xzf', 'artifact.php?name=' + neo4j_version + '.tar.gz', '-C', '/usr/lib/neo4j'],
            check=True)
        if out.returncode == 0:
            logging.info("Neo4j unpacked [success]")
        else:
            logging.error("Neo4j unpacked with error [error]")
        subprocess.run(["rm", 'artifact.php?name=' + neo4j_version + '.tar.gz'])
        logging.info("Neo4j installation is done")
        return


def config_neo4j():
    hostnumber = socket.gethostname()
    logging.info("Copying neo4j configuration file for hostnumber " + hostnumber)
    if 'neo4j-1' in hostnumber:
        subprocess.run(['sudo', 'cp', '/home/xnet/SDTD-Mazerunner/script/neo4j/conf/neo4j-1.conf',
                        '/usr/lib/neo4j/' + neo4j_path + '/conf/neo4j.conf'])
        logging.info("Importing database on neo4j-1...")
        subprocess.run(['sudo', 'rm', '-rf', '/usr/lib/neo4j/'+neo4j_path+'/data/databases/graph.db'])
        subprocess.run(['sudo', 'mkdir', '-p', '/usr/lib/neo4j/'+neo4j_path+'/data/databases/music.db'])
        subprocess.run(['sudo', '/usr/lib/neo4j/'+neo4j_path+'/bin/neo4j-import', '--into', '/usr/lib/neo4j/'+neo4j_path+'/data/databases/music.db', '--nodes', 'data/utilisateurs.csv', '--nodes', 'data/titres.csv', '--relationships', 'data/gout.csv'])
    elif 'neo4j-2' in hostnumber:
        subprocess.run(['sudo', 'cp', '/home/xnet/SDTD-Mazerunner/script/neo4j/conf/neo4j-2.conf',
                        '/usr/lib/neo4j/' + neo4j_path + '/conf/neo4j.conf'])
    elif 'neo4j-3' in hostnumber:
        subprocess.run(['sudo', 'cp', '/home/xnet/SDTD-Mazerunner/script/neo4j/conf/neo4j-3.conf',
                        '/usr/lib/neo4j/' + neo4j_path + '/conf/neo4j.conf'])
    return

def config_haproxy():
    hostnumber = socket.gethostname()
    if 'neo4j-3' in hostnumber:
        subprocess.run(['sudo', 'add-apt-repository', '-y', 'ppa:vbernat/haproxy-1.5'])
        subprocess.run(['sudo', 'apt-get', 'update'])
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'haproxy'])
    return

def set_database():
    logging.info("Importing database")
    subprocess.run(['sudo', 'mkdir', '/usr/lib/neo4j'+neo4j_path+'/data/databases/music.db'])
    subprocess.run(['sudo', '/usr/lib/neo4j/'+neo4j_path+'/bin/neo4j-import', '--into', '/usr/lib/neo4j/'+neo4j_path+'/data/databases/music.db', '--nodes', 'data/utilisateurs.csv', '--nodes', 'data/titres.csv', '--relationships', 'data/gout.csv'])

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    install_neo4j()
    config_neo4j()
    config_haproxy()
