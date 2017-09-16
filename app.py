import requests
import re
import random
import configparser
from bs4 import BeautifulSoup
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
#import sys  
#reload(sys)  
#sys.setdefaultencoding('utf-8')
app = Flask(__name__)

line_bot_api = LineBotApi('PebyWZbRffy3piwRInGduhL9BMkq/AjXB4SB7GVjInwdCKxmAg80VIjFHp4pgvrOGPW8UEuSwHJ318smi/06v9Ib1nHBWoG5W128O81Y3UsmuHjlPhdNPoxCtBNe6dW9b1j3p+9KutaXg1dIWep9UQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1023d2bc1b68157deb377644a1067c86')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def pattern_mega(text):
    patterns = [
        'mega', 'mg', 'mu', 'ＭＥＧＡ', 'ＭＥ', 'ＭＵ',
        'ｍｅ', 'ｍｕ', 'ｍｅｇａ', 'GD', 'MG', 'google',
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True


def eyny_movie():
    target_url = 'http://www.eyny.com/forum-205-1.html'
    print('Start parsing eynyMovie....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ''
    for titleURL in soup.select('.bm_c tbody .xst'):
        if pattern_mega(titleURL.text):
            title = titleURL.text
            if '11379780-1-3' in titleURL['href']:
                continue
            link = 'http://www.eyny.com/' + titleURL['href']
            data = '{}\n{}\n\n'.format(title, link)
            content += data
    return content



def beauty():
    target_url = 'https://www.ptt.cc/bbs/Beauty/index.html'
    rs=requests.get(target_url)
    res=rs.get(target_url,verify=False)
    soup=BeautifulSoup(rs.text,'html.parser')
    content=''
    for i in soup.select('.r-ent .title'):
        #title=i.text.encode('utf-8')
        #print(i.text)
        if pattern_mega(i.text):
            title = i.text
            if i.find('a'):
                link = 'https://www.ptt.cc'+i.find('a')['href']
                data = '{}\n{}\n\n'.format(title,link)
                content+=data
    return content



@handler.add(MessageEvent, message=TextMessage)
def handle_messag(event):
    if event.message.text == "eric":
        content = "XXXXXXXXXXXXXXXXXXXXXXXXX"
        content = eyny_movie()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    elif event.message.text == "beauty":
        content=beauty()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text))
        return 0

if __name__ == "__main__":
    app.run()
