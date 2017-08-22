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
from btsd import BTSDSpider
from yuanbao import YuanbaoSpider
from jubi import JubiSpider
from bijiu import BijiuSpider
from dahonghuo import DahonghuoSpider
from b8w import B8Spider
from coinvc import CoinVCSpider

import logger
import time
import random
import datetime

class MasterSpider:
    def __init__(self):
        self.config = Config()
        self.logger = logger.getLoggerFC('master_spider', self.config.master_spider_log)
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
            BTSDSpider(config=self.config,
                           database=self.database),
            YuanbaoSpider(config=self.config,
                       database=self.database),
            JubiSpider(config=self.config,
                          database=self.database),
            BijiuSpider(config=self.config,
                       database=self.database),
            CoinVCSpider(config=self.config,
                        database=self.database),
            DahonghuoSpider(config=self.config,
                         database=self.database),
            B8Spider(config=self.config,
                            database=self.database),
        ]

    def run(self):
        while True:
            print datetime.datetime.now(), "invoke master spider"
            number_of_news = self.invokeSpider()
            if number_of_news > 0 :
                self.logger.info(str(number_of_news) + " news discovered")
            time.sleep((random.random() * 120) + 60)

    def invokeSpider(self):
        newPush = []
        for eachSpider in self.spiders:
            newPush.extend(eachSpider.update())

        if newPush:
            self.sender.send(newPush)
        return len(newPush)


if __name__ == "__main__":
    masterSpider = MasterSpider()
    masterSpider.run()
