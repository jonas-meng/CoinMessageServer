#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup, Comment
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime

class BTSDSpider(Spider):
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.BTSD)

    def getArticleInfo(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select("li.shadow")

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None, None

        soup = BeautifulSoup(html, "html.parser")

        # obtain news date time
        t = soup.select('div.header')
        if not t:
            return None, None
        t = t[0].p.span.text
        t = datetime.datetime.strptime(t.strip(), '%Y-%m-%d %H:%M:%S')

        # remove redundant information
        content = soup.select(".article_con")
        if not content:
            return None, None
        content = content[0]

        content = str(content)
        return t, content

    def getArticleTitleAndLink(self, articleInfo):
        title = articleInfo.a.span.text
        link = articleInfo.a['href']
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = BTSDSpider(config, database)
    #sender.send(parser.update())
    parser.update()
