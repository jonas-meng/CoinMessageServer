#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import datetime
import logger
import time

from config import Config
from database import Database
from translate_helper import translate

class TwitterSpider:
    def __init__(self, config, database):
        self.config = config
        self.database = database
        self.logger = logger.getLoggerFC('Twitter', config.spider_log)

        self.twitter_ids = {
            config.website[config.POLONIEX]['twitter_id'].encode('utf-8') : config.POLONIEX,
            config.website[config.LIQUI]['twitter_id'].encode('utf-8') : config.LIQUI,
            config.website[config.BITSTAMP]['twitter_id'].encode('utf-8') : config.BITSTAMP,
            config.website[config.GDAX]['twitter_id'].encode('utf-8') : config.GDAX,
            config.website[config.COINCHECK]['twitter_id'].encode('utf-8') : config.COINCHECK,
        }
        twitter_credential = database.getTwitterCredential().find_one()
        self.consumer_key = twitter_credential['consumer_key']
        self.consumer_secret = twitter_credential['consumer_secret']

        self.access_token = twitter_credential['access_token']

        self.access_token_secret = twitter_credential['access_token_secret']

    def getHomeLline(self, api):
        try:
            public_tweets = api.home_timeline()
        except Exception as e:
            public_tweets = []
        return public_tweets

    def getBJTime(self):
        utc_dt = datetime.datetime.utcnow()
        td = datetime.timedelta(hours=8)
        bj_dt = utc_dt + td
        return bj_dt

    def update(self):
        oldArticles = self.database.getNewsCollection()

        newArticles = []

        auth = tweepy.OAuthHandler(self.consumer_key.encode('utf-8'), self.consumer_secret.encode('utf-8'))
        auth.set_access_token(self.access_token.encode('utf-8'), self.access_token_secret.encode('utf-8'))

        api = tweepy.API(auth)
        public_tweets = self.getHomeLline(api)
        if not public_tweets:
            time.sleep(3)
            public_tweets = self.getHomeLline(api)

        #public_tweets = api.home_timeline()
        for tweet in public_tweets:
            # only add one tweet
            #if len(newArticles) > 0:
            #    continue
            link = tweet.id_str

            if tweet.author.id_str in self.twitter_ids and not oldArticles.find_one({'link':link}):
                msg = self.config.website[self.twitter_ids[tweet.author.id_str]]['jpush_code'] + " - new article - " + link
                self.logger.info(msg)

                title = u"推特状态"
                notice = u'\n------------------------------------------------\n*以下是英文原文*\n'
                content = (translate(tweet.text) +
                           notice.encode('utf-8') +
                           tweet.text.encode('utf-8'))
                articleInfo = {"code": self.twitter_ids[tweet.author.id_str],
                               "title": title.encode('utf-8'),
                               #"time": tweet.created_at,
                               "time": self.getBJTime(),
                               "link": link,
                               "content": content}
                oldArticles.insert(articleInfo)
                newArticles.append(link)
        return newArticles


if __name__ == "__main__":
    config = Config()
    database = Database(config)
    twitterSpider = TwitterSpider(config, database)
    twitterSpider.update()
