#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup, Comment
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime

class HuobiProSpider(Spider):
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.HUOBIPRO)

    def getArticleInfo(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select(".page_notice_list_content")

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None, None

        soup = BeautifulSoup(html, "html.parser")

        content = soup.select_one(".page_notice_content")
        if not content:
            return None, None

        # obtain news date time
        #t = soup.select_one(".page_notice_time")
        #t = datetime.datetime.strptime(t.strip(), '%Y-%m-%d %H:%M:%S')
        t = datetime.datetime.now()

        content = str(content)
        return t, content

    def getArticleTitleAndLink(self, articleInfo):
        print(articleInfo)
        title = articleInfo.h2.text
        link = self.config.website[self.website_code]['domain'] + articleInfo['href']
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = HuobiProSpider(config, database)
    #sender.send(parser.update())
    parser.update()