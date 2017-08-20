#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import jpush
import json
import logger
import redis

from config import Config
from database import Database

pool = redis.ConnectionPool(host='localhost', port=6379)

class NewsPusher:
    def __init__(self, config, database):
        self.config = config
        self.logger = logger.getLoggerFC('pusher', config.pusher_log)
        self.database = database
        credential = database.getJpushCredential().find_one({})
        self.appKey = credential['appKey'].encode('utf-8')
        self.master_secret = credential['master_secret'].encode('utf-8')

    def cleanRedis(self, code):
        r = redis.Redis(connection_pool=pool)
        website_identity = 1 << code
        for key in r.keys():
            identity = int(key)
            if identity & website_identity:
                r.delete(identity)

    def callback(self, ch, method, properties, body):
        links = json.loads(body)
        news = self.database.getNewsCollection()

        _jpush = jpush.JPush(self.appKey, self.master_secret)

        for link in links:
            article = news.find_one({'link': link})
            if article is None:
                continue

            # update outdated cache
            self.cleanRedis(article['code'])

            pusher = _jpush.create_push()
            pusher.audience = jpush.audience(jpush.tag(self.config.website[article['code']]['jpush_code']))
            pusher.platform = jpush.all_
            pusher.notification = jpush.notification(alert=article['title'])
            self.logger.info("PUSH - " + self.config.website[article['code']]['jpush_code'] + " - " + link)

            try:
                response = pusher.send()
            except jpush.common.Unauthorized:
                raise jpush.common.Unauthorized("Unauthorized")
            except jpush.common.APIConnectionException:
                raise jpush.common.APIConnectionException("conn")
            except jpush.common.JPushFailure:
                print ("JPushFailure")
            except:
                print ("Exception")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def receive(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue = self.config.rabbit_push_news_queue)

        channel.basic_consume(self.callback,
                              queue = self.config.rabbit_push_news_queue)
        channel.start_consuming()

if __name__ == "__main__":
    config = Config()
    database = Database(config)
    newPusher = NewsPusher(config, database)
    newPusher.receive()