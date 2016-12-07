#!/usr/bin/env python3
import subprocess, logging

def stop_rabbitmq():
    subprocess.run(['sudo', 'rabbitmqctl', 'stop_app'])
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    stop_rabbitmq()