#!/usr/bin/python
# -*- coding:utf-8 -*-

from googletrans import Translator

translator = Translator()

def translate(text, src='en', dest='zh-cn'):
    res = translator.translate(text, src=src, dest=dest)
    translated_text = res.text.encode('utf-8')
    prettified_translated_text = translated_text.replace('</ ', '</')
    return prettified_translated_text


if __name__ == "__main__":
    with open('./output.html','r') as f:
        text = f.read()
        print translate(text)
