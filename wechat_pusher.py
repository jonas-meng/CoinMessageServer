#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import json
import datetime
import time

class WechatPusher:

    def __init__(self, config, app_id, app_secret, r):
        self.config = config
        self.app_id = app_id
        self.app_secret = app_secret
        self.redis_cache = r
        self.access_token_query = 'https://api.weixin.qq.com/cgi-bin/token?' \
                                  'grant_type=client_credential&appid=%s&secret=%s' \
                                  % (self.app_id, self.app_secret)
        self.get_user_list_query = 'https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s&next_openid=%s'
        self.next_openid = ''
        self.info_push_query = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s'
        self.template_id = 'XSLGMu3N8kAm9LH5cahSxpO0LoXCEiHFfIEgY4tslqY'
        self.info_push_template = {"touser": "",
                              "template_id": self.template_id,
                              "url": "",
                              "miniprogram": "",
                              "data": {}
                              }

    def obtain_access_token(self):

        if (self.redis_cache.exists('wechat_access_token')
            and self.redis_cache.exists('wechat_expire_time')
            and self.validateTime(self.redis_cache.get('wechat_expire_time'))):
           return self.redis_cache.get('wechat_access_token')
        else:
            response = self.request_get(self.access_token_query)
            if not response:
                return None

            result = response.json()
            access_token, expires_in = result['access_token'], result['expires_in']
            if not access_token:
                return None
            else:
                self.redis_cache.set('wechat_access_token', access_token)
                self.redis_cache.set('wechat_expire_time', self.get_expire_time(expires_in))
                return access_token

    def get_expire_time(self, expires_in):
        # 60 secs for padding
        expires_in = expires_in - 60
        now = datetime.datetime.now()
        time_delta = datetime.timedelta(seconds=expires_in)
        return now + time_delta

    def request_get(self, query):
        try:
            response = requests.get(query)
            response.raise_for_status()
        except requests.RequestException as e:
            return None
        else:
            return response

    def request_post(self, query, data):
        try:
            response = requests.post(query, data=data)
            response.raise_for_status()
        except requests.RequestException as e:
            return None
        else:
            return response

    def validateTime(self, expire_time):
        now = datetime.datetime.now()
        expire_time = datetime.datetime.strptime(expire_time, '%Y-%m-%d %H:%M:%S.%f')
        return now < expire_time

    def get_user_list(self, access_token, next_openid):
        query = self.get_user_list_query % (access_token, next_openid)
        response = self.request_get(query)
        if not response:
            return []

        result = response.json()
        self.next_openid = result['next_openid']
        return result['data']['openid']

    def push(self, article):
        platform = {'value': self.config.website[article['code']]['name'].encode('utf-8')}
        title = {'value': article['title'].encode('utf-8')}
        a_time = {'value': str(article['time']).encode('utf-8')}
        link = {'value': article['link'].encode('utf-8')}

        access_token = self.obtain_access_token()

        if not access_token:
            return None

        info_push_query = self.info_push_query % access_token
        while True:
            user_list = self.get_user_list(access_token, self.next_openid)
            if not user_list:
                # sleep 5 seconds and try again
                time.sleep(5)
                user_list = self.get_user_list(access_token, self.next_openid)
                if not user_list:
                    break

            self.info_push_template['data']['platform'] = platform
            self.info_push_template['data']['title'] = title
            self.info_push_template['data']['time'] = a_time
            self.info_push_template['data']['link'] = link

            for openid in user_list:
                self.info_push_template['touser'] = openid.encode('utf-8')
                info_push = json.dumps(self.info_push_template, ensure_ascii=False)

                response = self.request_post(info_push_query, data=info_push)
                if not response:
                    print 'Failed Wechat Push'

            # stop when current user list is the last one
            if user_list[-1] == self.next_openid:
                # reset to initial
                self.next_openid = ''
                break

if __name__ == "__main__":
    print 'wechat pusher'
