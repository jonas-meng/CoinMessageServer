#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime


class OKCoinSpider(Spider):
    '''
    OKCoin has some weired behavior that some of their announcements are not available,
    which would incur undesired issues on the spider
    '''
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.OKCOIN)

    def getArticleInfo(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select("li span.spanOne")

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None, None

        soup = BeautifulSoup(html, "html.parser")

        t = soup.select(".time")
        if not t:
            return None, None
        t = t[0].text
        t = datetime.datetime.strptime(t.strip(), '%Y-%m-%d %H:%M')

        content = soup.select(".invitation_content")
        if not content:
            return None, None
        return t, str(content[0])

    def getArticleTitleAndLink(self, articleInfo):
        title = articleInfo.a.text
        link = articleInfo.a['href']
        self.logger.info(title + " : " + link)
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = OKCoinSpider(config, database)
    #sender.send(parser.update())
    parser.update()
