#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup, Comment
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime

class BterSpider:
    def __init__(self, config, spider, database):
        self.config = config
        self.spider = spider
        self.database = database

    def getArticleInfo(self, link):
        html = self.spider.openUrl(link)
        if html is None:
            return None

        soup = BeautifulSoup(html, "html.parser")
        return soup.select(".entry")

    def getArticleContent(self, link):
        html = self.spider.openUrl(link)
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

    def updateDB(self, link):
        oldArticles = self.database.getNewsCollection()

        response = self.getArticleInfo(link)
        if response is None:
            return

        newArticles = []
        for articleInfo in reversed(response):
            #if (len(newArticles) > 0):
            #    continue
            title = articleInfo.a['title']
            link = self.config.website[self.config.BTER]['domain'] + articleInfo.a['href']
            count = oldArticles.count()

            if not oldArticles.find_one({'link':link}):

                formatedTime, content = self.getArticleContent(link)
                if content is None:
                    continue

                articleInfo = {"id": count,
                               "code": self.config.YUNBI,
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
        newPush.extend(self.updateDB(self.config.website[self.config.BTER]['link']))
        return newPush

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    spider = Spider(config)
    parser = BterSpider(config, spider, database)
    #sender.send(parser.update())
    parser.update()
