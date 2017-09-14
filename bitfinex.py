#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from config import Config
from spider import Spider
from sender import Sender
from database import Database
from translate_helper import translate

import datetime

class BitfinexSpider(Spider):
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.BITFINEX)

    def getArticleInfo(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select("#posts-page a.ajax")

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None, None

        soup = BeautifulSoup(html, "html.parser")

        # obtain news date time
        t = datetime.datetime.now()

        # remove redundant information
        content = soup.select("div.section")
        if not content:
            return None, None
        content = content[0]

        content = content.text
        content = translate(content) + '\n' + content
        return t, content

    def getArticleTitleAndLink(self, articleInfo):
        title = articleInfo.text.strip()
        link = self.config.website[self.website_code]['domain'] + articleInfo['href']
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = BitfinexSpider(config, database)
    #sender.send(parser.update())
    parser.update()
