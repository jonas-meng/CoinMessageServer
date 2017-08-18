#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
from pymongo import MongoClient
from config import Config
import urllib2
import time

class YunbiSpider:
    def __init__(self, config):
        self.config = config

    def getArticleInfo(self, link):
        response = urllib2.urlopen(link, timeout=5)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        return soup.select(".article-list-link")

    def getArticleContent(self, link):
        response = urllib2.urlopen(link, timeout=5)
        html = response.read()
        soup = BeautifulSoup(html, "html.parser")
        return str(soup.select(".article-content")[0])

    def readDB(self):
        conn = MongoClient(self.config.dbAddress, self.config.dbPort)
        db = conn.coin_message
        return db.yunbi

    def getArticlesInJson(self, limit=10):
        result = []
        articleInfoCollection = self.readDB()
        for articleInfo in articleInfoCollection.find({}).sort("id",-1).limit(limit):
            result.append({
            "website":{
            "name": articleInfo['website']['name'].encode('utf-8'),
            "logo": articleInfo['website']['logo'].encode('utf-8')
            },
            "title": articleInfo['title'].encode('utf-8'),
            "time": articleInfo['time'].encode('utf-8'),
            "content": articleInfo['content'].encode('utf-8')})
        return result

    def updateDB(self, link):
        oldArticles = self.readDB()
        # ATTENTION: test only
        # oldArticles.remove()

        for articleInfo in reversed(self.getArticleInfo(link)):
            title = articleInfo.text
            link = 'https://yunbi.zendesk.com' + articleInfo['href']
            count = oldArticles.count()
            if not oldArticles.find_one({'link':link}):
                timeArray = time.localtime(time.time())
                formatedTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                content = self.getArticleContent(link)
                articleInfo = {"id": count,
                "website":
                    {"name":"云币网",
                    "logo":"https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1502904824728&di=34ee91802f42536c973730386246bef6&imgtype=jpg&src=http%3A%2F%2Fimg0.imgtn.bdimg.com%2Fit%2Fu%3D1256965929%2C1781527151%26fm%3D214%26gp%3D0.jpg"},
                    "title":title,
                    "time": formatedTime,
                    "link":link,
                    "content": str(content)}
                oldArticles.insert(articleInfo)
                count += 1


    def update(self):
        self.updateDB(self.config.yunbiSystem)
        self.updateDB(self.config.yunbiBusiness)

if __name__ == "__main__":
    config = Config()
    spider = YunbiSpider(config)
    spider.update()
