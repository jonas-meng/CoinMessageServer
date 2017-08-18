#!/usr/bin/python
# -*- coding:utf-8 -*-

from config import Config

import requests

class Spider:

    def __init__(self, config):
        self.config = config

    def openUrl(self, url):
        try:
            response = requests.get(url,
                                    timeout = (self.config.http_connect_time,
                                               self.config.http_read_time))
            response.raise_for_status()
        except requests.RequestException as e:
            print "HTTP REQUEST HAS FAILED"
            print e
            return None
        else:
            return response.text
