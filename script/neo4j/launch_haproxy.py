import os
import logging
import subprocess

if __name__ == '__main__':
    subprocess.run(['/usr/sbin/haproxy', '-f', '/etc/haproxy/haproxy.cfg'])
