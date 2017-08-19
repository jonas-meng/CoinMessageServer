#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup, Comment
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime

class HuobiSpider(Spider):
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.HUOBI)

    def getArticleInfo(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select(".tit")

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")

        content = soup.select(".notice.detail")[0]

        # obtain news date time
        t = content.li.span.text
        t = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')

        content = str(content)
        return t, content

    def getArticleTitleAndLink(self, articleInfo):
        title = articleInfo.a.text
        link = self.config.website[self.website_code]['domain'] + articleInfo.a['href']
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = HuobiSpider(config, database)
    #sender.send(parser.update())
    parser.update()
