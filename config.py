#!/usr/bin/python
# -*- coding:utf-8 -*-

class Config:
    min_time_interval = 1 * 10
    max_time_interval = 5 * 10

    http_connect_time = 6
    http_read_time = 20

    rabbit_push_news_queue = 'push_news'

    host = '0.0.0.0'
    port = 3389

    dbAddress = '127.0.0.1'
    dbPort = 27017

    YUNBI = 0

    website = [
        {
            "jpush_code": u"YB",
            "name": u"云币网",
            "logo": u"https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1502904824728&di=34ee91802f42536c973730386246bef6&imgtype=jpg&src=http%3A%2F%2Fimg0.imgtn.bdimg.com%2Fit%2Fu%3D1256965929%2C1781527151%26fm%3D214%26gp%3D0.jpg",
            "link": [u'https://yunbi.zendesk.com/hc/zh-cn/sections/115001440667-%E7%B3%BB%E7%BB%9F%E5%85%AC%E5%91%8A?page=1',
                     u'https://yunbi.zendesk.com/hc/zh-cn/sections/115001437708-%E4%B8%9A%E5%8A%A1%E5%85%AC%E5%91%8A?page=1'],
        }
    ]
