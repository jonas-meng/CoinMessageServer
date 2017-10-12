#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from config import Config
from spider import Spider
from sender import Sender
from database import Database
from translate_helper import translate

import datetime

class BinanceInterSpider(Spider):
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.BAINT)

    def getArticleInfo(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select(".article-list-link")

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None, None

        soup = BeautifulSoup(html, "html.parser")
        t = datetime.datetime.now()
        content = soup.select(".article-content")
        if not content:
            return None, None
        content = content[0]

        content = content.text
        notice = u'\n------------------------------------------------\n*以下是英文原文*\n'
        content = (translate(content) +
                   notice.encode('utf-8') +
                   content.encode('utf-8'))
        return t, content

    def getArticleTitleAndLink(self, articleInfo):
        title = articleInfo.text
        link = self.config.website[self.website_code]['domain'] + articleInfo['href']
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = BinanceInterSpider(config, database)
    #sender.send(parser.update())
    parser.update()