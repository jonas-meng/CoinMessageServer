#!/usr/bin/python
# -*- coding:utf-8 -*-

from pymongo import MongoClient

class Database:
    def __init__(self, config):
        self.config = config

    def getNewsCollection(self):
        conn = MongoClient(self.config.dbAddress, self.config.dbPort)
        db = conn.coin_message
        return db.news

    def getJpushCredential(self):
        conn = MongoClient(self.config.dbAddress, self.config.dbPort)
        db = conn.jpush
        return db.credential
