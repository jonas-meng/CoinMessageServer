#!/usr/bin/python
# -*- coding:utf-8 -*-

class Config:
    min_time_interval = 1 * 10
    max_time_interval = 5 * 10

    # acceptable http connection and read time
    http_connect_time = 6
    http_read_time = 20
    http_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'}

    # rabbitmq news push queue
    rabbit_push_news_queue = 'push_news'

    # flask server host and port
    host = '0.0.0.0'
    port = 3389

    # mongodb address and port
    dbAddress = '127.0.0.1'
    dbPort = 27017

    # website code
    YUNBI = 0
    BTER = 1
    BINANCE = 2
    HUOBI = 3
    OKCOIN = 4
    CHBTC = 5
    BTCTRADE = 6
    BTSD = 7

    # website information
    website = [
        {
            "jpush_code": u"YB",
            "name": u"云币网",
            "logo": u"https://p12.zdassets.com/hc/settings_assets/1604264/115000110067/rUpcir5P4PoBxhxqUqXcSQ-Group.png",
            "link": [u'https://yunbi.zendesk.com/hc/zh-cn/sections/115001440667-%E7%B3%BB%E7%BB%9F%E5%85%AC%E5%91%8A?page=1',
                     u'https://yunbi.zendesk.com/hc/zh-cn/sections/115001437708-%E4%B8%9A%E5%8A%A1%E5%85%AC%E5%91%8A?page=1'],
            "domain": u'https://yunbi.zendesk.com',
        },
        {
            "jpush_code": u"BTR",
            "name": u"比特儿",
            "logo": u"http://www.wanbizu.com/uploads/allimg/170811/0K51224M-2.png",
            "link": [u"https://cn.bter.com/articlelist/ann"],
            "domain": u"https://cn.bter.com",
        },
        {
            "jpush_code": u"BA",
            "name": u"币安",
            "logo": u"https://www.binance.com/resources/img/logo-cn.svg",
            "link": [u"https://binance.zendesk.com/hc/zh-cn/sections/115000106672-%E4%B8%9A%E5%8A%A1%E5%85%AC%E5%91%8A"],
            "domain": u"https://binance.zendesk.com",
        },
        {
            "jpush_code": u"HB",
            "name": u"火币网",
            "logo": u"https://static.huobi.com/exchange/src/images/logo_10344.png",
            "link": [u"https://www.huobi.com/p/content/notice"],
            "domain": u"https://www.huobi.com",
        },
        {
            "jpush_code": u"OK",
            "name": u"币行Okcoin",
            "logo": u"https://img.bafang.com/v_20170816001/okcoin/image/new_v1/logoNew.png",
            "link": [u"https://www.okcoin.cn/service.html?currentPage=1"],
            "domain": u"https://www.okcoin.cn",
        },
        {
            "jpush_code": u"CH",
            "name": u"中国比特币",
            "logo": u"https://s.chbtc.com/statics/img/v2/common/chbtc_logo.png",
            "link": [u"https://www.chbtc.com/i/blog?type=proclamation"],
            "domain": u"https://www.chbtc.com",
        },
        {
            "jpush_code": u"BT",
            "name": u"比特币交易网",
            "logo": u"https://www.btctrade.com/img/lang/cn/logo.jpg?v=1.2",
            "link": [u"https://www.btctrade.com/gonggao/"],
            "domain": u"https://www.chbtc.com",
        },
        {
            "jpush_code": u"BTSD",
            "name": u"比特时代",
            "logo": u"http://www.btc38.com/statics/img/sdc_logo.png",
            "link": [u'http://www.btc38.com/company_notices.html'],
            "domain": u'http://www.btc38.com',
        },
    ]
