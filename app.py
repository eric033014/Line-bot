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

app = Flask(__name__)

line_bot_api = LineBotApi('1023d2bc1b68157deb377644a1067c86')
handler = WebhookHandler('qPVeCIsgGmFCi5mkRuWwTwAm0cvDzIEyZrceVtz9Gl5/XPPOHoaeh8KusjGNI01/GPW8UEuSwHJ318smi/06v9Ib1nHBWoG5W128O81Y3UseKpqLpclp9V3viwJmmfEfrEbrvYAXIDatEVKzbr5lHwdB04t89/1O/w1cDnyilFU=')


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()