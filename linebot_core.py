# Linebot_Python_project
# Linebot code
# 載入需要的模組

from __future__ import unicode_literals
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

import configparser

import random

app = Flask(__name__)

"""
line-bot的基本資料 (建立一個config.ini的配置檔)

#Config.ini
[line-bot]
channel_access_token = oBtOINSU4GH40UshPoPtus6uEMdhz+YMGnsM74QPNRmEyfHK9I8rim/TiSpewb8AehJeELeetqtx3H/CQ5BSm2ZWJaUYrg7bMR21IJu7MSnW1skjtF+jwjK8ThQCFkFvJAwJraa4T4TLw+guvC/QTwdB04t89/1O/w1cDnyilFU=
channel_secret = 991ef928a89f1b5557e7a88954bceea4
"""

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        print(body, signature)
        handler.handle(body, signature)

    except InvalidSignatureError:
        abort(400)

    return 'OK'


# 學你說話
@handler.add(MessageEvent, message=TextMessage)
def pretty_echo(event):
    if event.source.user_id != "Udeadbeefdeadbeefdeadbeefdeadbeef":

        # Phoebe 愛唱歌
        pretty_note = '♫♪♬'
        pretty_text = ''

        for i in event.message.text:
            pretty_text += i
            pretty_text += random.choice(pretty_note)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=pretty_text)
        )
