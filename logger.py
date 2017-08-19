#!/usr/bin/python
# -*- coding:utf-8 -*-

import logging

def getLoggerFC(name, logFile):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    fh = logging.FileHandler(logFile)
    ch = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

def getLoggerF(logFile):
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)

    fh = logging.FileHandler(logFile)

    formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

    return logger

if __name__ == "__main__":
    log = getLoggerFC('log/test.log')
    log.info("why so many times?")
