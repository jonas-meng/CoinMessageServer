#!/usr/bin/python
# -*- coding:utf-8 -*-

from pymongo import MongoClient
from config import Config

class Database:

    def __init__(self, config):
        self.config = config
        self.conn = MongoClient(self.config.dbAddress, self.config.dbPort)

    def getNewsCollection(self):
        db = self.conn.coin_message
        return db.news

    def getJpushCredential(self):
        db = self.conn.jpush
        return db.credential

    def getWechatCredential(self):
        db = self.conn.wechat
        return db.credential

    def getTwitterCredential(self):
        db = self.conn.twitter
        return db.credential

    def getTelegramCredential(self):
        db = self.conn.telegram
        return db.credential

if __name__ == '__main__':
    config = Config()
    database = Database(config)
    articles = database.getNewsCollection()
    res = articles.find_one({'link':'https://www.bitfinex.com/posts/216'})
    print res['content']
    html = (u'<!DOCTYPE html><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><html><body>{0}</body></html>'.format(
        res['content']))
    print html