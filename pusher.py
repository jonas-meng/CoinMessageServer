#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import jpush
import json
import logger
import redis

from config import Config
from database import Database
from jpusher import JPusher
from wechat_pusher import WechatPusher

pool = redis.ConnectionPool(host='localhost', port=6379)

class NewsPusher:
    def __init__(self, config, database):
        self.config = config
        self.logger = logger.getLoggerFC('pusher', config.pusher_log)
        self.database = database
        credential = database.getJpushCredential().find_one({})
        self.appKey = credential['appKey'].encode('utf-8')
        self.master_secret = credential['master_secret'].encode('utf-8')

        wechat_credential = database.getWechatCredential().find_one({})
        self.app_id = wechat_credential['app_id']
        self.app_secret = wechat_credential['app_secret']

        self.pusher_list = [
            JPusher(config, self.app_key, self.master_secret),
            WechatPusher(config, self.app_id, self.app_secret, redis.Redis(connection_pool=pool))
        ]

    def cleanRedis(self, code):
        r = redis.Redis(connection_pool=pool)
        website_identity = 1 << code
        for key in r.keys():
            if key == 'wechat_access_token' or key == 'wechat_expire_time':
                continue
            identity = int(key)
            if identity & website_identity:
                r.delete(identity)

    def callback(self, ch, method, properties, body):
        links = json.loads(body)
        news = self.database.getNewsCollection()

        for link in links:
            article = news.find_one({'link': link})
            if article is None:
                continue

            # update outdated cache
            self.cleanRedis(article['code'])

            for pusher in self.pusher_list:
                pusher.push(article)

            print article['title'], article['link']

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