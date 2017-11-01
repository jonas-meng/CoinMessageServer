#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, request, render_template
from flask.ext import restful
from flask.ext.restful import reqparse
from config import Config
from database import Database
from sender import Sender

import json
import logging
import redis
import datetime

app = Flask(__name__)
api = restful.Api(app)
config = Config()
database = Database(config)
app_sender = Sender(config)
pool = redis.ConnectionPool(host='localhost', port=6379)

# add log file handler
file_handler = logging.FileHandler(config.server_log)
file_handler.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)

@api.representation('text/html')
def output_json(data, code, headers=None):
    response = app.make_response(data)
    #json.dumps(data, ensure_ascii=False))
    response.headers.extend(headers or {'Content-type':'text/html; charset=utf-8'})
    #response.headers.set('Access-Control-Allow-Origin', '*')
    return response

def getArticlesInJson(identity, website_codes, limit=10):
    result = []
    r = redis.Redis(connection_pool=pool)
    key = str(identity)
    if not r.exists(key):
        #result = json.loads(r.get(key), encoding='utf-8')
        articleInfoCollection = database.getNewsCollection()
        for articleInfo in articleInfoCollection\
            .find({'code': {'$in': website_codes}})\
            .sort("time",-1).limit(limit):
            result.append({
            "website":{
            "name": config.website[articleInfo['code']]['name'].encode('utf-8'),
            "code": config.website[articleInfo['code']]['jpush_code'].encode('utf-8'),
            },
            "title": articleInfo['title'].encode('utf-8'),
            "time": str(articleInfo['time']).encode('utf-8'),
            "content": articleInfo['content'].encode('utf-8')})
        if not r.exists(key):
            r.set(key, json.dumps({"posts": result}, ensure_ascii=False))
    return r.get(key)

def getSingleArticleInJson(url):
    result = ""
    r = redis.Redis(connection_pool=pool)
    key = str(url)
    #if not r.exists(key):
    if True:
        articleInfoCollection = database.getNewsCollection()
        cursor = articleInfoCollection.find_one({"link":url})
        if cursor:
            result = cursor['content']
            #if not r.exists(key):
            #    r.set(key, result, ex=3600)
    #res = (u'<!DOCTYPE html><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><html><body><h3>{0}</h3></body></html>')
    #res = res.format(result.replace('\n', '<br/>'))
    #return res.encode('utf-8')
    return render_template('index.html', content=result.split('\n'))

def storeArticleInDB(code, title, time, link,  content):
    code = int(code)
    time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
    articleCollection = database.getNewsCollection()
    if not articleCollection.find_one({'link':link}):
        articleInfo = {"code": code,
                       "title": title,
                       "time": time,
                       "link": link,
                       "content": content}

        articleCollection.insert(articleInfo)
    app_sender.send([link])

def identity2code(identity):
    idx = 0
    website_codes = []
    while identity:
        if identity & 1:
            website_codes.append(idx)
        identity = identity >> 1
        idx = idx + 1
    return website_codes

class Announcement(restful.Resource):
    def parserGetRequest(self):
        parser = reqparse.RequestParser()
        #parser.add_argument('identity', type=int)
        #parser.add_argument('number', type=int)
        parser.add_argument('url')
        return parser.parse_args()

    def parserPutRequest(self):
        parser = reqparse.RequestParser()
        parser.add_argument('time')
        parser.add_argument('title')
        parser.add_argument('content')
        return parser.parse_args()

    def get(self):
        args = self.parserGetRequest()
        '''
        return getArticlesInJson(
            args['identity'],
            identity2code(args['identity']),
            args['number'])
        '''
        return getSingleArticleInJson(args['url'])

    def put(self):
        storeArticleInDB(
            request.form.get('code'),
            request.form.get('title'),
            request.form.get('time'),
            request.form.get('link'),
            request.form.get('content'),
        )
        return 'Successful'

api.add_resource(Announcement, '/api/news')

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host=config.host, port=config.port, threaded=True)
