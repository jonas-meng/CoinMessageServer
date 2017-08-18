#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask
from flask.ext import restful
from flask.ext.restful import reqparse
from yunbi import YunbiSpider
from config import Config

import time
import json

app = Flask(__name__)
api = restful.Api(app)
config = Config()

@api.representation('application/json')
def output_json(data, code, headers=None):
    response = app.make_response(json.dumps(data, ensure_ascii=False))
    response.headers.extend(headers or {})
    response.headers.set('Access-Control-Allow-Origin', '*')
    return response

class Announcement(restful.Resource):
    spiders = [YunbiSpider(config)]

    def parserRequest(self):
        parser = reqparse.RequestParser()
        parser.add_argument('identity', type=int)
        parser.add_argument('number', type=int)
        return parser.parse_args()

    def get(self):
        args = self.parserRequest()
        identity = args['identity']
        number = args['number']

        result = []
        idx = 0
        while identity:
            if (identity& 1):
                result.extend(self.spiders[idx].getArticlesInJson(number))
            idx += 1
            identity = identity >> 1
        return {"posts":result}

api.add_resource(Announcement, '/api/getNews')

if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host=config.host, port=config.port)
