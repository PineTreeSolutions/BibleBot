# Copyright (C) 2022 NuclearPine

import os, requests, random, math, bible, re
from flask import Flask
from flask import request
import telegram as tg

app = Flask(__name__)

secret_token = str(math.floor(random.random() * 10000))
if tg.setWebhook(os.getenv('TG_WEBHOOK_URL'), secret_token)['ok'] != True:
    raise Exception('Failure to set webhook')

# test method
@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.headers['X-Telegram-Bot-Api-Secret-Token'] != secret_token:
        tg.setWebhook(os.getenv('TG_WEBHOOK_URL'), secret_token)
        return {'ok' : True}
    else:
        update = request.json
        if 'text' not in update['message']:
            return {'ok' : True}
        elif (re.search('^/bible ', update['message']['text']) != None):
            response = bible.fetch_verses(re.sub('^/bible ', '', update['message']['text']))
            tg.sendMessage(chat_id=update['message']['chat']['id'], text=response)
            return {'ok' : True}
        else:
            return {'ok' : True}

