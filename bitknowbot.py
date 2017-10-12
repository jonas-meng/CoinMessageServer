#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests

class BitKnowBot:
    query_template = "https://api.telegram.org/bot{0}/{1}"

    method_names = ["sendMessage"]
    channel_names = [u"@bitknowinfo"]

    def __init__(self, token):
        self.token = token

    def obtain_query(self, method_name):
        return self.query_template.format(self.token, method_name)

    def obtain_send_data(self, chat_id, text):
        return {"chat_id": chat_id.encode("utf-8"),
                "text": text.encode("utf-8")}

    def obtain_text(self, article):
        pass

    def push(self, article, pool):
        response = requests.post(self.obtain_query(self.method_names[0]),
                      data=self.obtain_send_data(self.channel_names[0], article["content"]))
        print(response.json())

if __name__ == "__main__":
    pass
