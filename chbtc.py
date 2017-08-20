#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime


class CHBTCSpider(Spider):
    '''
    The time stamp on CHBTC is bit weired.
    What we get is in form of %Y-%m-%d %H:%M:%S.%f, whereas it appears on website as %Y-%m-%d %H:%M
    '''
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.CHBTC)

    def getArticleInfo(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select("article.envor-post")

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None, None

        soup = BeautifulSoup(html, "html.parser")

        t = soup.select("div.page-right")
        t = t[0].select("span")
        if not t:
            return None, None
        t = t[0].text
        t = datetime.datetime.strptime(t.strip(), '%Y-%m-%d %H:%M')

        content = soup.select("article.page-content")
        if not content:
            return None, None
        return t, str(content[0])

    def getArticleTitleAndLink(self, articleInfo):
        tag_a = articleInfo.header.h3.a
        title = tag_a.text
        link = self.config.website[self.website_code]['domain'] + tag_a['href']
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = CHBTCSpider(config, database)
    #sender.send(parser.update())
    parser.update()
