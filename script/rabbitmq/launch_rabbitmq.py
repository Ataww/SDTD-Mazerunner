#!/usr/bin/env python3
import subprocess, logging

def launch_rabbitmq():
    subprocess.run(['sudo', 'rabbitmqctl', 'start_app'])
    return

def launch_haproxy():
    subprocess.run(['sudo','service','haproxy','start'])
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    launch_haproxy()
    launch_rabbitmq()