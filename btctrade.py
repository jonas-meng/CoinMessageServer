#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime


class BtcTradeSpider(Spider):
    '''
    BTCTrqade accept https request but not http request
    '''
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.BTCTRADE)

    def getArticleInfo(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select("div.hd")

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None, None

        soup = BeautifulSoup(html, "html.parser")

        t = soup.select("div.news_title")
        t = t[0].dl.dd.text
        if not t:
            return None, None
        t = datetime.datetime.strptime(t.strip(), '%Y-%m-%d')

        content = soup.select("div.news_desc")
        if not content:
            return None, None
        return t, str(content[0])

    def getArticleTitleAndLink(self, articleInfo):
        tag_a = articleInfo.a
        title = tag_a.text
        link = 'https://' + tag_a['href'][7:]
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = BtcTradeSpider(config, database)
    #sender.send(parser.update())
    parser.update()
