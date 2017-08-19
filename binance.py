#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime

class BinanceSpider(Spider):
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.BINANCE)

    def getArticleInfo(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select(".article-list-link")

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        t = datetime.datetime.now()
        return t, str(soup.select(".article-content")[0])

    def getArticleTitleAndLink(self, articleInfo):
        title = articleInfo.text
        link = self.config.website[self.website_code]['domain'] + articleInfo['href']
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = BinanceSpider(config, database)
    #sender.send(parser.update())
    parser.update()
