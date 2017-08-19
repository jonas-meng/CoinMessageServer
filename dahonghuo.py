#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup, Comment
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime

class DahonghuoSpider(Spider):
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.DHH)

    def getArticleInfo(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select("div.info_list_con")

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None, None

        soup = BeautifulSoup(html, "html.parser")

        # obtain news date time
        t = soup.select('div.info_show_t span')
        if not t:
            return None, None
        t = t[2].text
        t = datetime.datetime.strptime(t.strip(), '%Y-%m-%d')

        # remove redundant information
        content = soup.select("div.info_show")
        if not content:
            return None, None
        content = content[0]

        content = str(content)
        return t, content

    def getArticleTitleAndLink(self, articleInfo):
        title = articleInfo.h2.a.text.strip()
        link = self.config.website[self.website_code]['domain'] + articleInfo.h2.a['href']
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = DahonghuoSpider(config, database)
    #sender.send(parser.update())
    parser.update()
