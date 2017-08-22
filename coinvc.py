#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup, Comment
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import datetime
import requests

class CoinVCSpider(Spider):
    '''
    seems like coinvc has used some special ssl verification technique, blocking unverified visit
    '''
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.BJS)
        self.start_date = '1970-01-01 20:00:00'
        self.start_date = datetime.datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")

    def getArticleInfo(self, link):
        html = self.openSpecialUrl(link)
        if html is None:
            return None

        result = html
        return result['resultList']

    def openSpecialUrl(self, url):
        try:
            response = requests.get(url, headers=self.config.http_header,
                                    timeout=(self.http_connect_time,
                                             self.http_read_time))
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.exception(e)
            return None
        else:
            try:
                result = response.json()
            except:
                return None
            else:
                return result


    def getArticleContent(self, link):
        html = self.openSpecialUrl(link)
        if html is None:
            return None, None

        result = html
        time_delta = datetime.timedelta(milliseconds=result['date'])
        t = self.start_date + time_delta
        now = datetime.datetime.now()
        if t > now:
            t = now
        return t, result['content'].encode('utf-8')

    def getArticleTitleAndLink(self, articleInfo):
        title = articleInfo['title']
        link = self.config.website[self.website_code]['link'][0] + articleInfo['_id']
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = CoinVCSpider(config, database)
    #sender.send(parser.update())
    parser.update()
