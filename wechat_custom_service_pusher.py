#!/usr/bin/python
# -*- coding:utf-8 -*-

from wechat_pusher import WechatPusher
from config import Config
from multiprocessing import Pool
import json
import redis
import datetime

class WechatCustomServicePusher(WechatPusher):
    def __init__(self, config, app_id, app_secret, r):
        WechatPusher.__init__(self, config, app_id, app_secret, r)
        self.custom_service_query = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s'
        self.custom_service_template = {
            "touser":"",
            "msgtype":"news",
            "news":{
                "articles": [
                    {
                        "title": "",
                        "description": "",
                        "url":"",
                        "picurl":""
                    },
                ]
            }
        }

    def data_generate(self, article):
        formated_article = {}
        formated_article['title'] = article['title'].encode('utf-8')
        formated_article['description'] = (u"公告平台：%s \n公告时间：%s \n\n>>点击查看官网详情<<" % (
            self.config.website[article['code']]['name'],
            article['time'].strftime("%Y-%m-%d %H:%M:%S")
        ))
        formated_article['description'] = formated_article['description'].encode('utf-8')

        if article['code'] != 11:
            formated_article['url'] = article['link'].encode('utf-8')
        else:
            # https://api.coinvc.com/api/v2/getNews/59a117ed5b2fec581f1520db
            # https://www.coinvc.com/news/59a117ed5b2fec581f1520db
            link = article['link'].encode('utf-8')
            formated_article['url'] = 'https://www.coinvc.com/news/' + link.split('/')[-1]
            formated_article['url'] = formated_article['url'].encode('utf-8')

        self.custom_service_template['news']['articles'][0] = formated_article

    def get_post_data(self, openid):
        self.custom_service_template['touser'] = openid.encode('utf-8')
        return json.dumps(self.custom_service_template, ensure_ascii=False)

    def get_post_query(self, access_token):
        return (self.custom_service_query % access_token)

    def get_target_user_list(self, access_token):
        all_user_list = self.get_all_user(access_token)
        white_list_user = self.get_tagged_user_list(access_token, self.config.white_list_tag)
        non_white_list_user = all_user_list - white_list_user
        return non_white_list_user

if __name__ == "__main__":
    config = Config()
