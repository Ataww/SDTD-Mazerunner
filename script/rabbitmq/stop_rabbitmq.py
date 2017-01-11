#!/usr/bin/env python3
import subprocess, logging

def stop_rabbitmq():
    subprocess.run(['sudo', 'rabbitmqctl', 'stop_app'])
    return

def stop_haproxy():
    subprocess.run(['sudo','service','haproxy','stop'])
    return

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,format="%(asctime)s :: %(levelname)s :: %(message)s")
    stop_haproxy()
    stop_rabbitmq()