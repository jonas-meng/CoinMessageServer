#!/usr/bin/python
# -*- coding:utf-8 -*-


import pika
import json

class Sender:
    def __init__(self, config):
        self.config = config

    def send(self, data):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue = self.config.rabbit_push_news_queue)

        channel.basic_publish(exchange = '',
                              routing_key = self.config.rabbit_push_news_queue,
                              body = json.dumps(data))
        connection.close()