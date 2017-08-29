#!/usr/bin/python
# -*- coding:utf-8 -*-

from wechat_pusher import WechatPusher
from config import Config
import json
import redis
import datetime
import time

class WechatTemplatePusher(WechatPusher):
    def __init__(self, config, app_id, app_secret, r):
        WechatPusher.__init__(self, config, app_id, app_secret, r)
        self.template_query = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s'
        self.template_id = 'fNsetwlJIdso2gb_IC5eTGxnpqVeMnz9_WLEJYlx7k4'
        self.info_template = {"touser": "",
                              "template_id": self.template_id,
                              "url": "",
                              "miniprogram": "",
                              "data": {}
                              }

    def data_generate(self, article):
        remark = u'感谢关注跟进'
        first = (u'项目平台：%s' % self.config.website[article['code']]['name'])
        self.info_template['data'] = {
            'first' : {'value': first.encode('utf-8')},
            'keyword1' : {'value': 'BIZHIDAO'},
            'keyword2' : {'value': article['title'].encode('utf-8')},
            'keyword3' : {'value': article['time'].strftime("%Y-%m-%d %H:%M:%S").encode('utf-8')},
            'remark' : {'value': remark.encode('utf-8')}
        }
        if article['code'] != 11:
            self.info_template['url'] = article['link'].encode('utf-8')
        else:
            # https://api.coinvc.com/api/v2/getNews/59a117ed5b2fec581f1520db
            # https://www.coinvc.com/news/59a117ed5b2fec581f1520db
            link = article['link'].encode('utf-8')
            self.info_template['url'] = 'https://www.coinvc.com/news/' + link.split('/')[-1]
            self.info_template['url'] = self.info_template['url'].encode('utf-8')

    def get_post_data(self, openid):
        self.info_template['touser'] = openid.encode('utf-8')
        return json.dumps(self.info_template, ensure_ascii=False)

    def get_post_query(self, access_token):
        return (self.template_query % access_token)

if __name__ == "__main__":
    config = Config()