#!/usr/bin/python
# -*- coding:utf-8 -*-

import jpush

class JPusher:
    def __init__(self, config, appKey, master_secret):
        self.config = config
        self.appKey = appKey
        self.master_secret = master_secret

    def push(self, article):
        _jpush = jpush.JPush(self.appKey, self.master_secret)

        pusher = _jpush.create_push()
        pusher.audience = jpush.audience(jpush.tag(self.config.website[article['code']]['jpush_code']))
        pusher.platform = jpush.all_
        pusher.notification = jpush.notification(alert=article['title'])

        try:
            response = pusher.send()
            # send for IOS
            pusher.options = {'apns_production': False}
            response = pusher.send()
        except jpush.common.Unauthorized:
            raise jpush.common.Unauthorized("Unauthorized")
        except jpush.common.APIConnectionException:
            raise jpush.common.APIConnectionException("APIConnection Failed")
        except jpush.common.JPushFailure:
            print 'JpushFailure'
        except:
            print "Unknow except"

if __name__ == "__main__":
    print 'hello to jpusher'
