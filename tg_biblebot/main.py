# Copyright (C) 2022 NuclearPine

import os, requests
from flask import Flask
from flask import request

webhook_url = os.getenv('TG_WEBHOOK')
bot_token = os.getenv('TG_TOKEN')

app = Flask(__name__)

# test method
@app.route('/', methods=['GET', 'POST'])
def webhook():
    return {success : True}