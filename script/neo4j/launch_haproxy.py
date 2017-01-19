import os
import logging
import subprocess

if __name__ == '__main__':
    subprocess.run(['/usr/sbin/haproxy', '-f', '/home/xnet/SDTD-Mazerunner/script/neo4j/conf/haproxy.cfg'])
