#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup, Comment
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime

class BterSpider(Spider):
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.BTER)

    def getArticleInfo(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select(".entry")

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")

        # obtain news date time
        t = soup.select('.new-dtl-info')[0].span.text
        t = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')

        # remove redundant information
        content = soup.select(".dtl-content")[0]
        content.select(".prenext")[0].extract()
        content.select("#snsshare")[0].extract()
        content.select("style")[0].extract()
        comments = content.find_all(text = lambda text: isinstance(text, Comment))
        [comment.extract() for comment in comments]

        content = str(content)
        return t, content

    def getArticleTitleAndLink(self, articleInfo):
        title = articleInfo.a['title']
        link = self.config.website[self.website_code]['domain'] + articleInfo.a['href']
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = BterSpider(config, database)
    #sender.send(parser.update())
    parser.update()
