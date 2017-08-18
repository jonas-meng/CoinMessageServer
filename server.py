#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse
from config import Config
from database import Database

import json

app = Flask(__name__)
api = restful.Api(app)
config = Config()
database = Database(config)

@api.representation('application/json')
def output_json(data, code, headers=None):
    response = app.make_response(json.dumps(data, ensure_ascii=False))
    response.headers.extend(headers or {})
    response.headers.set('Access-Control-Allow-Origin', '*')
    return response

def getArticlesInJson(website_codes, limit=10):
    result = []
    articleInfoCollection = database.getNewsCollection()
    for articleInfo in articleInfoCollection\
            .find({'code': {'$in': website_codes}})\
            .sort("id",-1).limit(limit):
        result.append({
        "website":{
        "name": config.website[articleInfo['code']]['name'].encode('utf-8'),
        "logo": config.website[articleInfo['code']]['logo'].encode('utf-8'),
        },
        "title": articleInfo['title'].encode('utf-8'),
        "time": articleInfo['time'].encode('utf-8'),
        "content": articleInfo['content'].encode('utf-8')})
    return result

def identity2code(identity):
    idx = 0
    website_codes = []
    while identity:
        if (identity & 1):
            website_codes.append(idx)
        identity = identity >> 1
        idx = idx + 1
    return website_codes

class Announcement(restful.Resource):

    def parserRequest(self):
        parser = reqparse.RequestParser()
        parser.add_argument('identity', type=int)
        parser.add_argument('number', type=int)
        return parser.parse_args()

    def get(self):
        args = self.parserRequest()
        return {"posts": getArticlesInJson(
            identity2code(args['identity']),
            args['number'])}

api.add_resource(Announcement, '/api/getNews')

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host=config.host, port=config.port)
