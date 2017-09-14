#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from config import Config
from spider import Spider
from sender import Sender
from database import Database
from translate_helper import translate

import datetime

class KrakenSpider(Spider):
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.KRAKEN)

    def getArticleInfo(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select(".entry-title")

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None, None

        soup = BeautifulSoup(html, "html.parser")

        # obtain news date time
        t = datetime.datetime.now()

        # remove redundant information
        content = soup.select("article.post")
        if not content:
            return None, None
        content = content[0]

        content = content.text
        notice = u'\n------------------------------------------------\n*以下是英文原文*\n'
        content = (translate(content) +
                   notice.encode('utf-8') +
                   content.encode('utf-8'))
        print content
        return t, content

    def getArticleTitleAndLink(self, articleInfo):
        title = articleInfo.a.text.strip()
        title = translate(title)
        link = articleInfo.a['href']
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = KrakenSpider(config, database)
    #sender.send(parser.update())
    parser.update()
