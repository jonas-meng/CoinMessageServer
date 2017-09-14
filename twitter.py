#!/usr/bin/python
# -*- coding: utf-8 -*-

import tweepy
import datetime

from config import Config
from database import Database
from translate_helper import translate

class TwitterSpider:
    def __init__(self, config, database):
        self.config = config
        self.database = database

        self.twitter_ids = {
            config.website[config.POLONIEX]['twitter_id'].encode('utf-8') : config.POLONIEX,
            config.website[config.LIQUI]['twitter_id'].encode('utf-8') : config.LIQUI,
        }
        twitter_credential = database.getTwitterCredential()
        self.consumer_key = twitter_credential['consumer_key']
        self.consumer_secret = twitter_credential['consumer_secret']
        self.access_token = twitter_credential['access_token']
        self.access_token_secret = twitter_credential['access_token_secret']

    def update(self):
        oldArticles = self.database.getNewsCollection()

        newArticles = []

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        api = tweepy.API(auth)

        public_tweets = api.home_timeline()
        for tweet in public_tweets:
            # only add one tweet
            #if len(newArticles) > 0:
            #    continue
            link = tweet.id_str

            if tweet.author.id_str in self.twitter_ids and not oldArticles.find_one({'link':link}):
                title = u"推特状态"
                notice = u'\n------------------------------------------------\n*以下是英文原文*\n'
                content = (translate(tweet.text) +
                           notice.encode('utf-8') +
                           tweet.text.encode('utf-8'))
                articleInfo = {"code": self.twitter_ids[tweet.author.id_str],
                               "title": title.encode('utf-8'),
                               "time": tweet.created_at,
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
