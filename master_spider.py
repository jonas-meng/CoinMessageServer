#!/usr/bin/python
# -*- coding:utf-8 -*-

from config import Config
from database import Database
from sender import Sender
from yunbi import YunbiSpider
from bter import BterSpider
from binance import BinanceSpider
from huobi import HuobiSpider
from okcoin import OKCoinSpider
from chbtc import CHBTCSpider
from btctrade import BtcTradeSpider

class MasterSpider:
    def __init__(self):
        self.config = Config()
        self.database = Database(self.config)
        self.sender = Sender(self.config)
        self.spiders = [
            YunbiSpider(config=self.config,
                        database=self.database),
            BterSpider(config=self.config,
                        database=self.database),
            BinanceSpider(config=self.config,
                       database=self.database),
            HuobiSpider(config=self.config,
                        database=self.database),
            OKCoinSpider(config=self.config,
                        database=self.database),
            CHBTCSpider(config=self.config,
                        database=self.database),
            BtcTradeSpider(config=self.config,
                        database=self.database),
        ]

    def run(self):
        newPush = []
        for eachSpider in self.spiders:
            newPush.extend(eachSpider.update())
        if newPush:
            self.sender.send(newPush)

if __name__ == "__main__":
    masterSpider = MasterSpider()
    masterSpider.run()
