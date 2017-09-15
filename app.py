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

line_bot_api = LineBotApi('qPVeCIsgGmFCi5mkRuWwTwAm0cvDzIEyZrceVtz9Gl5/XPPOHoaeh8KusjGNI01/GPW8UEuSwHJ318smi/06v9Ib1nHBWoG5W128O81Y3UseKpqLpclp9V3viwJmmfEfrEbrvYAXIDatEVKzbr5lHwdB04t89/1O/w1cDnyilFU=')
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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    if enent.message.text == 'eyny':
	content=movie()
	line_bot_api.reply_message(
	    event.reply_token,
            TextSendMessage(text=content))
        return 0


def movie():
    target_url = 'http://www.eyny.com/forum-205-1.html'
    rs=requests.session()
    res=rs.get(target_url,verify=False)
    soup=BeautifulSoup(res.text,'html.parser')
    content=''
    for title in soup.select('.bm_c tbody .xst'):
	if pattern_mega(title.text)
	    titletext=title.text
`	    link='http://www.eyny/com/'+title['href']
	    data='{}\n{}\n\n'.format(title,link)
	    content += data
    return content



if __name__ == "__main__":
    app.run(i)
