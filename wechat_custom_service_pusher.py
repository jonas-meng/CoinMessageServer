#!/usr/bin/python
# -*- coding:utf-8 -*-

from wechat_pusher import WechatPusher
from config import Config
import json
import redis
import datetime

class WechatCustomServicePusher(WechatPusher):
    def __init__(self, config, app_id, app_secret, r):
        WechatPusher.__init__(self, config, app_id, app_secret, r)
        self.custom_service_query = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token=%s'
        self.custom_service_template = {"touser": "",
                                        "msgtype": 'text',
                                        'text':{
                                            'content': ''
                                        }
                                        }

    def data_generate(self, article):
        content = u'欢迎来到币知道小助手'
        self.custom_service_template['text']['content'] = content.encode('utf-8')

    def get_post_data(self, openid):
        self.custom_service_template['touser'] = openid.encode('utf-8')
        return json.dumps(self.custom_service_template, ensure_ascii=False)

    def get_post_query(self, access_token):
        return (self.custom_service_query % access_token)

if __name__ == "__main__":
    config = Config()
