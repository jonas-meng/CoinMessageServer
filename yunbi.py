#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime

class YunbiSpider:
    def __init__(self, config, spider, database):
        self.config = config
        self.spider = spider
        self.database = database
        self.website_code = config.YUNBI

    def getArticleInfo(self, link):
        html = self.spider.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select(".article-list-link")

    def getArticleContent(self, link):
        html = self.spider.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return str(soup.select(".article-content")[0])

    def updateDB(self, link):
        oldArticles = self.database.getNewsCollection()

        response = self.getArticleInfo(link)
        if response is None:
            return []

        newArticles = []
        for articleInfo in reversed(response):
            #if (len(newArticles) > 0):
            #    continue
            title = articleInfo.text
            link = self.config.website[self.website_code]['domain'] + articleInfo['href']
            count = oldArticles.count()

            if not oldArticles.find_one({'link':link}):

                content = self.getArticleContent(link)
                if content is None:
                    continue

                articleInfo = {"id": count,
                               "code": self.website_code,
                               "title":title,
                               "time": datetime.datetime.now(),
                               "link":link,
                               "content": str(content)}

                oldArticles.insert(articleInfo)
                newArticles.append(count)
                count += 1
        return newArticles

    def update(self):
        newPush = []
        newPush.extend(self.updateDB(self.config.website[self.website_code]['link'][0]))
        newPush.extend(self.updateDB(self.config.website[self.website_code]['link'][1]))
        return newPush

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    spider = Spider(config)
    parser = YunbiSpider(config, spider, database)
    #sender.send(parser.update())
    parser.update()
