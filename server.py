#!/usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask
from flask.ext import restful
from yunbi import YunbiSpider
from config import Config

import json

app = Flask(__name__)
api = restful.Api(app)

@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = app.make_response(json.dumps(data, ensure_ascii=False))
    resp.headers.extend(headers or {})
    return resp

config = Config()
spiders = [YunbiSpider(config)]

class Announcement(restful.Resource):
    def get(self, identity):
        result = []
        idx = 0
        while identity:
            if (identity& 1):
                result.extend(spiders[idx].getArticlesInJson(1))
            idx += 1
            identity = identity >> 1
        return {"posts":result}

api.add_resource(Announcement, '/<int:identity>')

if __name__ == '__main__':
    app.run(debug=True)
