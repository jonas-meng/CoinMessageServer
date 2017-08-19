#!/usr/bin/python
# -*- coding:utf-8 -*-

from config import Config
from database import Database
from sender import Sender
from yunbi import YunbiSpider
from bter import BterSpider
from binance import BinanceSpider
from huobi import HuobiSpider
from spider import Spider

class MasterSpider:
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
            BinanceSpider(config=self.config,
                       database=self.database,
                       spider=self.spider),
            HuobiSpider(config=self.config,
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
    masterSpider = MasterSpider()
    masterSpider.run()
