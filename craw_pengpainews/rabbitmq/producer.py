#!/usr/bin/env python
# -*- coding: utf_8 -*-

import pika

from craw_pengpainews.rabbitmq import Constants


def emit(message):
    # 创建连接connection到localhost
    user_pwd = pika.PlainCredentials('baoming', 'baoming')

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='115.29.108.4', credentials=user_pwd))
    channel = connection.channel()

    channel.exchange_declare(exchange=Constants.exchange_name,
                             exchange_type=Constants.exchange_type)

    channel.basic_publish(exchange=Constants.exchange_name,
                          routing_key=Constants.route_key,
                          body=message)

    connection.close()


if __name__ == '__main__':
    emit("message test 222")
