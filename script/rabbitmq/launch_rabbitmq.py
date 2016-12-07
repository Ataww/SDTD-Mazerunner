#!/usr/bin/env python3
import subprocess, logging

def launch_rabbitmq():
    subprocess.run(['sudo', 'rabbitmqctl', 'start_app'])
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    launch_rabbitmq()