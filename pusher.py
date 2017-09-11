#!/usr/bin/python
# -*- coding:utf-8 -*-

import pika
import jpush
import json
import logger
import redis
import datetime

from multiprocessing import Pool
from config import Config
from database import Database
from jpusher import JPusher
from wechat_template_pusher import WechatTemplatePusher
from wechat_custom_service_pusher import WechatCustomServicePusher
from foreign_pusher import FPusher

pool = redis.ConnectionPool(host='localhost', port=6379)

process_pool = Pool()

class NewsPusher:
    def __init__(self, config, database):
        self.config = config
        self.logger = logger.getLoggerFC('pusher', config.pusher_log)
        self.database = database
        credential = database.getJpushCredential().find_one({})
        self.app_key = credential['appKey'].encode('utf-8')
        self.master_secret = credential['master_secret'].encode('utf-8')

        wechat_credential = database.getWechatCredential().find_one({})
        self.app_id = wechat_credential['app_id'].encode('utf-8')
        self.app_secret = wechat_credential['app_secret'].encode('utf-8')

        self.pusher_list = [
            JPusher(config, self.app_key, self.master_secret),
            WechatTemplatePusher(config, self.app_id, self.app_secret, redis.Redis(connection_pool=pool), self.config.white_list_tag),
            WechatCustomServicePusher(config, self.app_id, self.app_secret, redis.Redis(connection_pool=pool))
        ]

        self.foreign_pusher_list = [
            FPusher(config)
        ]

        self.vip_pusher_list = [
            WechatTemplatePusher(config, self.app_id, self.app_secret, redis.Redis(connection_pool=pool), self.config.test_tag),
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

            msg = '%s %s' % (article['title'].encode('utf-8'), article['link'].encode('utf-8'))
            self.logger.info(msg)

            print datetime.datetime.now(), article['title'], article['link']
            if not self.config.is_on_foreign_server:
                if article['code'] < self.config.BITFINEX:
                    for pusher in self.pusher_list:
                        pusher.push(article, pool=process_pool)
                else:
                    # article pusher only for vip
                    for pusher in self.vip_pusher_list:
                        pusher.push(article, pool=process_pool)
            else:
                for pusher in self.foreign_pusher_list:
                    pusher.push(article, pool=process_pool)

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def receive(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',  heartbeat_interval=0))
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