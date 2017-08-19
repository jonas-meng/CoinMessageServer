#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup, Comment
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime

class YuanbaoSpider(Spider):
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.YBW)

    def getArticleInfo(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select("li.hideli")

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None, None

        soup = BeautifulSoup(html, "html.parser")

        # obtain news date time
        t = soup.select('div.product.left.clearfix')
        t = t[0].find("p")
        if not t:
            return None, None
        t = t.text
        t = datetime.datetime.strptime(t.strip(), '%Y-%m-%d %H:%M')

        # remove redundant information
        content = soup.select(".paragraph.paragraph_news")
        if not content:
            return None, None
        content = content[0]

        content = str(content)
        return t, content

    def getArticleTitleAndLink(self, articleInfo):
        title = articleInfo.a.text.strip()
        link = self.config.website[self.website_code]['domain'] +  articleInfo.a['href']
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = YuanbaoSpider(config, database)
    #sender.send(parser.update())
    parser.update()
