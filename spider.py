#!/usr/bin/python
# -*- coding:utf-8 -*-

from config import Config
from database import Database

import requests
import logger
import time
import random
import datetime

class Spider:

    def __init__(self, config, database, website_code):
        self.config = config
        # not specifying name would result in redundant log record
        self.logger = logger.getLoggerFC(config.website[website_code]['jpush_code'], config.spider_log)
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
            self.logger.exception(e)
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

    def validateTime(self, article_time):
        t = datetime.datetime.now()
        allowed_time_delta_pos = datetime.timedelta(minutes=4)
        allowed_time_delta_neg = datetime.timedelta(minutes=-4)
        real_time_delta = t - article_time
        if real_time_delta < allowed_time_delta_pos \
                and real_time_delta > allowed_time_delta_neg:
            return article_time
        else:
            return t

    def getBJTime(self):
        utc_dt = datetime.datetime.utcnow()
        td = datetime.timedelta(hours=8)
        bj_dt = utc_dt + td
        return bj_dt

    def updateDB(self, link):
        oldArticles = self.database.getNewsCollection()

        response = self.getArticleInfo(link)
        if response is None:
            return []

        newArticles = []
        for articleInfo in reversed(response):
            # TEST ONLY
            #if (len(newArticles) > 0):
            #   continue
            title, link = self.getArticleTitleAndLink(articleInfo)
            if not link:
                continue

            if not oldArticles.find_one({'link':link}):
                # to avoid blocking by the website
                # sleep for x secs, where x is larger than 1 and smaller than 5
                time.sleep(random.random() * 3)

                formatedTime, content = self.getArticleContent(link)
                if content is None or formatedTime is None:
                    continue
                #formatedTime = self.validateTime(formatedTime)
                formatedTime = self.getBJTime()

                msg = self.config.website[self.website_code]['jpush_code'] + " - new article - " + link
                self.logger.info(msg)

                articleInfo = {"code": self.website_code,
                               "title":title,
                               "time": formatedTime,
                               "link":link,
                               "content": str(content)}

                oldArticles.insert(articleInfo)
                newArticles.append(link)
        return newArticles

if __name__ == "__main__":
    config = Config()
    database = Database(config)
    spider = Spider(config, database, config.YUNBI)
    spider.openUrl(u"https://www.coinvc.com/news")
