# Copyright (C) 2022 NuclearPine
import os, requests

baseurl = f'https://api.telegram.org/bot{os.getenv("TG_TOKEN")}/'

def setWebhook(url: str, secret_token: str):
    payload = {
        'url' : url,
        'secret_token' : secret_token
    }
    r = requests.get(url=baseurl + 'setWebhook', data=payload)
    return r.json()

def deleteWebhook():
    r = requests.get(url=baseurl + 'deleteWebhook')
    return r.json()

def sendMessage(chat_id, text):
    payload = {
        'chat_id' : chat_id,
        'text' : text,
        'parse_mode' : 'HTML'
    }
    r = requests.get(url=baseurl + 'sendMessage', data=payload)
    return r.json()