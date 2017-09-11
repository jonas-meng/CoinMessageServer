#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests

class FPusher:
    def __init__(self, config):
        self.config = config

    def push(self, article, pool):
        url = self.config.domestic_pusher_url
        data = {
            'code': article['code'],
            'time': article['time'].strftime("%Y-%m-%d %H:%M:%S").encode('utf-8'),
            'title': article['title'].encode('utf-8'),
            'link': article['link'].encode('utf-8'),
            'content': article['content'].encode('utf-8'),
        }
        res = requests.put(url=url, data=data)
        print res.text

if __name__ == "__main__":
    print 'hello to jpusher'