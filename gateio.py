#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime

class GateIOSpider(Spider):
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.GATEIO)

    def getArticleInfo(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select(".entry")

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None, None

        soup = BeautifulSoup(html, "html.parser")
        t = datetime.datetime.now()
        content = soup.select(".dtl-content")
        if not content:
            return None, None
        return t, str(content[0])

    def getArticleTitleAndLink(self, articleInfo):
        title = articleInfo.a['title']
        link = self.config.website[self.website_code]['domain'] + articleInfo.a['href']
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = GateIOSpider(config, database)
    parser.update()
