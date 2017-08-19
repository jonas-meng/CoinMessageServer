#!/usr/bin/python
# -*- coding:utf-8 -*-

from config import Config
from database import Database

import requests

class Spider:

    def __init__(self, config, database, website_code):
        self.config = config
        self.database = database
        self.header = config.http_header
        self.http_connect_time = config.http_connect_time
        self.http_read_time = config.http_read_time
        self.website_code = website_code

    def openUrl(self, url):
        try:
            response = requests.get(url, headers=self.header,
                                    timeout = (self.http_connect_time,
                                               self.http_read_time))
            response.raise_for_status()
        except requests.RequestException as e:
            print "HTTP REQUEST HAS FAILED"
            print e
            return None
        else:
            return response.text

    def getArticleInfo(self, link):
        return None

    def getArticleContent(self, link):
        return None, None

    def getArticleTitleAndLink(self, articleInfo):
        return None, None

    def update(self):
        newPush = []
        for link in self.config.website[self.website_code]['link']:
            newPush.extend(self.updateDB(link))
        return newPush

    def updateDB(self, link):
        oldArticles = self.database.getNewsCollection()

        response = self.getArticleInfo(link)
        if response is None:
            return []

        newArticles = []
        for articleInfo in reversed(response):
            # TEST ONLY
            #if (len(newArticles) > 0):
            #    continue
            title, link = self.getArticleTitleAndLink(articleInfo)
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

if __name__ == "__main__":
    config = Config()
    database = Database(config)
    spider = Spider(config, database, config.YUNBI)
    spider.openUrl(u"https://www.btctrade.com/gonggao/2680.html")
