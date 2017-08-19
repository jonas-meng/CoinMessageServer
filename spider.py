#!/usr/bin/python
# -*- coding:utf-8 -*-

from config import Config


import requests

class Spider:

    def __init__(self, config):
        self.config = config
        self.header = config.http_header
        self.http_connect_time = config.http_connect_time
        self.http_read_time = config.http_read_time

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

if __name__ == "__main__":
    config = Config()
    spider = Spider(config)
    spider.openUrl(u"https://www.huobi.com/p/content/notice")
