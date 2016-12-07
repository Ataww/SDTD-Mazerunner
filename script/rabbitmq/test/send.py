#!/usr/bin/env python3

import argparse, pika

parser = argparse.ArgumentParser()
parser.add_argument('host', help="RabbitMQ hostname")
parser.add_argument('user', help="RabbitMQ user")
parser.add_argument('password', help="RabbitMQ password")
args = parser.parse_args()

credentials = pika.PlainCredentials(args.user, args.password)
connection = pika.BlockingConnection(pika.ConnectionParameters(args.host,5672,'/', credentials))
channel = connection.channel()

channel.queue_declare(queue='hello', durable=True)

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!',
                      properties=pika.BasicProperties(
                        delivery_mode = 2,
                      ))

print(" [x] Sent 'Hello World!'")
connection.close()
