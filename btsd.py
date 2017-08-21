#!/usr/bin/python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup, Comment
from config import Config
from spider import Spider
from sender import Sender
from database import Database

import requests

import datetime

class BTSDSpider(Spider):
    headers = {'content-type': 'application/json',
               'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    def __init__(self, config, database):
        Spider.__init__(self, config, database, config.BTSD)

    def getArticleInfo(self, link):
        notice = self.openSpecialUrl(link)
        if notice is None:
            return None

        return notice

    def openSpecialUrl(self, url):
        try:
            response = requests.post(url, data={'target': 1, 'page': 1}, headers=self.headers)
            response.raise_for_status()
        except requests.RequestException as e:
            self.logger.exception(e)
            return None
        else:
            result = response.json()
            return result['notice']

    def getArticleContent(self, link):
        html = self.openUrl(link)
        if html is None:
            return None, None

        soup = BeautifulSoup(html.encode('ISO-8859-1'), "html.parser")

        # obtain news date time
        t = soup.select('div.header')
        if not t:
            return None, None
        t = t[0].p.span.text
        t = datetime.datetime.strptime(t.strip(), '%Y-%m-%d %H:%M:%S')

        # remove redundant information
        content = soup.select(".article_con")
        if not content:
            return None, None
        content = content[0]

        content = str(content)
        return t, content

    def getArticleTitleAndLink(self, articleInfo):
        title = articleInfo['title']
        link = articleInfo['url']
        return title, link

if __name__ == "__main__":
    config = Config()
    sender = Sender(config)
    database = Database(config)
    parser = BTSDSpider(config, database)
    #sender.send(parser.update())
    parser.update()
