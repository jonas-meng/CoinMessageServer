#!/usr/bin/python
# -*- coding:utf-8 -*-

from googletrans import Translator
from bs4 import UnicodeDammit

translator = Translator()

def divideText(text):
    res = []
    last = len(text)
    first = len(text) - 5000
    while first > 0:
        idx = text.find('.', first)
        first = idx + 1
        res.append(text[first:last])
        last = first
        first = idx - 5000
    if last > 0:
        res.append(text[0:last])
    return reversed(res)

def translate(text, src='en', dest='zh-cn', enable_emoji=False):
    if enable_emoji:
        text = text.encode("unicode-escape")
    text_list = []
    if len(text) < 5000:
        text_list = [text]
    else:
        text_list = divideText(text)

    translated_text_list = []
    for each_text in text_list:
        res = translator.translate(each_text, src=src, dest=dest)
        translated_text = res.text
        translated_text_list.append(translated_text)
    result = ''.join(translated_text_list)
    return result.encode('utf-8')

if __name__ == "__main__":
    print translate(u"我是好人")
    print translate(u"RT @mihar: I'm looking for a Senior Backend Engineer - GDAX https://t.co/WoXOQySVyH - RT please 🙏")
