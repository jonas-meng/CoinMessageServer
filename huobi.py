#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup, Comment
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime

class HuobiSpider:
    def __init__(self, config, spider, database):
        self.config = config
        self.spider = spider
        self.database = database
        self.website_code = config.HUOBI

    def getArticleInfo(self, link):
        html = self.spider.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select(".tit")

    def getArticleContent(self, link):
        html = self.spider.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")

        content = soup.select(".notice.detail")[0]

        # obtain news date time
        t = content.li.span.text
        t = datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')

        content = str(content)
        return t, content

    def updateDB(self, link):
        oldArticles = self.database.getNewsCollection()

        response = self.getArticleInfo(link)
        if response is None:
            return []

        newArticles = []
        for articleInfo in reversed(response):
            #if (len(newArticles) > 0):
            #    continue
            title = articleInfo.a.text
            link = self.config.website[self.website_code]['domain'] + articleInfo.a['href']
            count = oldArticles.count()

            if not oldArticles.find_one({'link':link}):

                formatedTime, content = self.getArticleContent(link)
                if content is None:
                    continue

                articleInfo = {"id": count,
                               "code": self.website_code,
                               "title":title,
                               "time": formatedTime,
                               "link":link,
                               "content": str(content)}

                oldArticles.insert(articleInfo)
                newArticles.append(count)
                count += 1
        return newArticles

    def update(self):
        newPush = []
        newPush.extend(self.updateDB(self.config.website[self.website_code]['link']))
        return newPush

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    spider = Spider(config)
    parser = HuobiSpider(config, spider, database)
    #sender.send(parser.update())
    parser.update()
