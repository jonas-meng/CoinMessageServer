#!/usr/bin/env bash
pip install virtualenv
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
makedir log

# sudo apt-get install mongo
# sudo apt-get install rabbitmq-server
