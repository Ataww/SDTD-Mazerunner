#!/usr/bin/env python3
import pika, argparse

parser = argparse.ArgumentParser()
parser.add_argument('host', help="RabbitMQ hostname")
parser.add_argument('user', help="RabbitMQ user")
parser.add_argument('password', help="RabbitMQ password")
args = parser.parse_args()

credentials = pika.PlainCredentials(args.user, args.password)
connection = pika.BlockingConnection(pika.ConnectionParameters(args.host,5672,'/', credentials))
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(callback,
                      queue='hello',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()