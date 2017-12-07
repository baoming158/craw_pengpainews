#!/usr/bin/env python
import pika
import Constants
import Task


def comsume():

    user_pwd = pika.PlainCredentials('baoming', 'baoming')

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='115.29.108.4', credentials=user_pwd))

    channel = connection.channel()

    channel.exchange_declare(exchange=Constants.exchange_name,
                             exchange_type=Constants.exchange_type)

    channel.queue_declare(queue=Constants.queue_name)

    channel.queue_bind(exchange=Constants.exchange_name,
                       queue=Constants.queue_name, routing_key=Constants.route_key)

    print(' [*] Waiting for logs. To exit press CTRL+C')

    channel.basic_consume(Task.callback,
                          queue=Constants.queue_name,
                          no_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    comsume()
