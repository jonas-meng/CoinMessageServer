#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup, Comment
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime

class JubiSpider(Spider):
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.JUBI)

    def getArticleInfo(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select("a.title")

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None, None

        soup = BeautifulSoup(html, "html.parser")

        # obtain news date time
        t = soup.select('span.pub_date')
        if not t:
            return None, None
        t = t[0].text
        t = datetime.datetime.strptime(t.strip(), '%Y-%m-%d')

        # remove redundant information
        content = soup.select(".about_text")
        if not content:
            return None, None
        content = content[0]
        content.select("div.guess")[0].extract()

        content = str(content)
        return t, content

    def getArticleTitleAndLink(self, articleInfo):
        title = articleInfo.text.strip()
        link = self.config.website[self.website_code]['domain'] + articleInfo['href']
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = JubiSpider(config, database)
    #sender.send(parser.update())
    parser.update()
