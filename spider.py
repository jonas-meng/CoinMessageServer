#!/usr/bin/python
# -*- coding:utf-8 -*-

from config import Config
from database import Database
from sender import Sender
from yunbi import YunbiSpider
from bter import BterSpider

import requests

class Spider:

    def __init__(self, config):
        self.config = config

    def openUrl(self, url):
        try:
            response = requests.get(url,
                                    timeout = (self.config.http_connect_time,
                                               self.config.http_read_time))
            response.raise_for_status()
        except requests.RequestException as e:
            print "HTTP REQUEST HAS FAILED"
            print e
            return None
        else:
            return response.text

class MotherSpider:
    def __init__(self):
        self.config = Config()
        self.database = Database()
        self.sender = Sender()
        self.spider = Spider()
        self.spiders = [
            YunbiSpider(config=self.config,
                        database=self.database,
                        spider=self.spider),

            BterSpider(config=self.config,
                        database=self.database,
                        spider=self.spider),
        ]

    def run(self):
        newPush = []
        for eachSpider in self.spiders:
            newPush.extend(eachSpider.update())
        if not newPush:
            self.sender.send(newPush)

if __name__ == "__main__":
    motherSpider = MotherSpider()
    motherSpider.run()
