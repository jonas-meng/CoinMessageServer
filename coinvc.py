#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup, Comment
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime

class CoinVCSpider(Spider):
    '''
    seems like coinvc has used some special ssl verification technique, blocking unverified visit
    '''
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.BJS)

    def getArticleInfo(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        body = soup.select("div.panel-body")
        return body[0].select("div.pull-left")

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None, None

        soup = BeautifulSoup(html, "html.parser")

        # obtain news date time
        t = soup.select('div.panel-heading')
        if not t:
            return None, None
        t = t[0].select("span.ng-binding")
        if not t:
            return None, None
        t = t[0].text
        t = datetime.datetime.strptime(t.strip(), '%Y-%m-%d %H:%M:%S')

        # remove redundant information
        content = soup.select("div.panel-body")
        if not content:
            return None, None
        content = content[0]

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
    parser = CoinVCSpider(config, database)
    #sender.send(parser.update())
    parser.update()
