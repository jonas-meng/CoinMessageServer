#!/usr/bin/python
# -*- coding:utf-8 -*-

import requests
import datetime
import time
import redis
import json

from multiprocessing import Pool

def request_post(query, data):
    try:
        response = requests.post(query, data=data)
        response.raise_for_status()
    except requests.RequestException as e:
        return None
    else:
        return response

def send_post_request(query, data, openid):
    response = request_post(query=query, data=data)
    if not response:
        print 'Failed Wechat Push'
    else:
        result = response.json()
        # error code returned, indicating information push failure
        if result.get('errcode'):
            print result
    print datetime.datetime.now(), ('send data to %s user' % openid)

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
        self.count = 0
        self.get_user_with_tag_query = 'https://api.weixin.qq.com/cgi-bin/user/tag/get?access_token=%s'

    def request_access_token(self):
        response = self.request_get(self.access_token_query)
        if not response:
            return None, None

        result = response.json()
        access_token = result.get('access_token')
        expires_in = result.get('expires_in')
        if not access_token:
            return None, None
        return access_token, expires_in

    def obtain_access_token(self):
        #if (self.redis_cache.exists('wechat_access_token')
        #    and self.redis_cache.exists('wechat_expire_time')
        #    and self.validateTime(self.redis_cache.get('wechat_expire_time'))):
        if False:
            return self.redis_cache.get('wechat_access_token')
        else:
            access_token, expires_in = self.request_access_token()
            if not access_token:
                # try again after 3 second
                time.sleep(3)
                access_token, expires_in = self.request_access_token()
                if not access_token:
                    return None

            self.redis_cache.set('wechat_access_token', access_token)
            self.redis_cache.set('wechat_expire_time', self.get_expire_time(expires_in))
            return access_token

    def get_expire_time(self, expires_in):
        # 600 secs for padding
        expires_in = expires_in - 1200
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

    def validateTime(self, expire_time):
        now = datetime.datetime.now()
        expire_time = datetime.datetime.strptime(expire_time, '%Y-%m-%d %H:%M:%S.%f')
        return now < expire_time

    def request_user_list(self, access_token, next_openid):
        query = self.get_user_list_query % (access_token, next_openid)
        response = self.request_get(query)
        if not response:
            return []

        result = response.json()
        data = result.get('data')
        if not data:
            return []

        openid_list = data.get('openid')
        if not openid_list:
            return []
        else:
            self.next_openid = result.get('next_openid')
            self.count = result.get('count')
            return  openid_list

    def request_tagged_user(self, access_token, next_openid, tag):
        query = self.get_user_with_tag_query % access_token
        # white list tag id 101
        data = { "tagid" : tag, "next_openid": next_openid }
        response = request_post(query, json.dumps(data))
        if not response:
            return []

        result = response.json()
        data = result.get('data')
        if not data:
            return []

        openid_list = data.get('openid')
        if not openid_list:
            return []
        else:
            self.next_openid = result.get('next_openid')
            self.count = result.get('count')
            return openid_list

    def obtain_user_list(self, access_token, next_openid):
        user_list = self.request_user_list(access_token, self.next_openid)
        if not user_list:
            # sleep 3 seconds and try again
            time.sleep(3)
            user_list = self.request_user_list(access_token, self.next_openid)
            if not user_list:
                return None
        return user_list

    def data_generate(self, article):
        return {}

    def get_post_query(self, access_toekn):
        return {}

    def get_post_data(self, openid):
        return '{}'

    def get_target_user_list(self, access_token):
        return {}

    def get_tagged_user_list(self, access_token, tag):
        tagged_user_list = set()
        self.next_openid = ''
        # obtain user white list
        while True:
            user_list = self.request_tagged_user(access_token, self.next_openid, tag)
            if not user_list:
                break
            tagged_user_list.update(user_list)

            if self.count == 0:
                self.next_openid = ''
                break
        return tagged_user_list

    def get_all_user(self, access_token):
        all_user_list = set()
        self.next_openid = ''
        # obtain all user
        while True:
            user_list = self.obtain_user_list(access_token, self.next_openid)
            if not user_list:
                break
            all_user_list.update(user_list)

            # stop when current user list is the last one
            if self.count == 0:
                # reset to initial
                self.next_openid = ''
                break
        return all_user_list

    def push(self, article, pool):
        access_token = self.obtain_access_token()
        if not access_token:
            return None

        target_user_list = self.get_target_user_list(access_token)

        self.data_generate(article)

        for openid in target_user_list:
            query = self.get_post_query(access_token)
            data = self.get_post_data(openid)
            #pool.apply_async(send_post_request, args=(query, data, openid))
            pool.add_task({'func': send_post_request, 'args': {'query': query, 'data': data, 'openid': openid}})


if __name__ == "__main__":
    print 'wechat pusher'

