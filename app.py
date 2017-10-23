import random
import requests
import re
import random
import configparser
import urllib
from bs4 import BeautifulSoup
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
)
#import sys  
#reload(sys)  
#sys.setdefaultencoding('utf-8')
app = Flask(__name__)

line_bot_api = LineBotApi('PebyWZbRffy3piwRInGduhL9BMkq/AjXB4SB7GVjInwdCKxmAg80VIjFHp4pgvrOGPW8UEuSwHJ318smi/06v9Ib1nHBWoG5W128O81Y3UsmuHjlPhdNPoxCtBNe6dW9b1j3p+9KutaXg1dIWep9UQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('1023d2bc1b68157deb377644a1067c86')

bang=['https://truth.bahamut.com.tw/s01/201708/61df0d65bccde69c70d5f9d0240c74be.JPG','https://truth.bahamut.com.tw/s01/201708/a94cb92b9f6d7c76ed30c987d5cafe6b.JPG','https://truth.bahamut.com.tw/s01/201708/5c838041e5b423c1d6d29f5db93a8ae4.JPG','https://scontent.ftpe5-1.fna.fbcdn.net/v/t1.0-9/21270956_342990686139577_1216760829687952297_n.jpg?oh=e267eef4a3ea2f69247a32bed94976d1&oe=5A170A9D','https://scontent.ftpe5-1.fna.fbcdn.net/v/t1.0-9/21231615_506045473083847_177753384360284829_n.jpg?oh=2558a1f409bb2aec85dbdb58c5a5398f&oe=5A50C4F7','https://scontent.ftpe5-1.fna.fbcdn.net/v/t1.0-9/21151549_511834835832124_7309600245286435106_n.jpg?oh=290e072b64c91bd60098c1d943bee62a&oe=5A137812','https://scontent.ftpe5-1.fna.fbcdn.net/v/t1.0-9/20841014_336605396788043_2673432232091169936_n.jpg?oh=1a977e9202f79aceea9495b0319f54d8&oe=5A5B2768']



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


def get_page_number(content):
    start_index = content.find('index')
    end_index = content.find('.html')
    page_number = content[start_index + 5: end_index]
    return int(page_number) + 1


def craw_page(res, push_rate):
    soup_ = BeautifulSoup(res.text, 'html.parser')
    article_seq = []
    for r_ent in soup_.find_all(class_="r-ent"):
        try:
            # 先得到每篇文章的篇url
            link = r_ent.find('a')['href']
            if link:
                # 確定得到url再去抓 標題 以及 推文數
                title = r_ent.find(class_="title").text.strip()
                rate = r_ent.find(class_="nrec").text
                url = 'https://www.ptt.cc' + link
                if rate:
                    rate = 100 if rate.startswith('爆') else rate
                    rate = -1 * int(rate[1]) if rate.startswith('X') else rate
                else:
                    rate = 0
                # 比對推文數
                if int(rate) >= push_rate:
                    article_seq.append({
                        'title': title,
                        'url': url,
                        'rate': rate,
                    })
        except Exception as e:
            # print('crawPage function error:',r_ent.find(class_="title").text.strip())
            print('本文已被刪除', e)
    return article_seq




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
    print("parsing beauty")
    requests.packages.urllib3.disable_warnings()
    rs=requests.session()
    res=rs.get(target_url,verify=False)
    soup=BeautifulSoup(res.text,'html.parser')
    content=''
    for i in soup.find_all(class_="r-ent"):
        #title=i.text.encode('utf-8')
        #print(i.text)
        if i.find('a'):
            title=i.find(class_="title").text.strip()
            link = 'https://www.ptt.cc'+i.find('a')['href']

            data = '{}\n{}\n\n'.format(title,link)
            content+=data
            print(data)
    print(content)
    return content


def tran(date,time):
    url = 'http://www.thsrc.com.tw/tw/TimeTable/SearchResult'
    print("highway station ing ")
    request= urllib.request.Request(url)
    request.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")

    form_data = {
        "StartStation": "977abb69-413a-4ccf-a109-0272c24fd490", 
        "EndStation": "fbd828d8-b1da-4b06-a3bd-680cdca4d2cd",
        "SearchDate": date,
        "SearchTime": time,
        "SearchWay":"DepartureInMandarin",
        "RestTime":"",
        "EarlyOrLater":""
    }
    print(form_data["StartStation"])
    form_data = urllib.parse.urlencode(form_data).encode("utf-8")
    response = urllib.request.urlopen(request,data=form_data)  
    html = response.read()
    soup= BeautifulSoup(html, 'html.parser')
    content=''
    for i in soup.find_all(class_="touch_table"):
        t=u"車次"
        trainnumber="車次"+str(i.find(class_="column1").text)
        print(trainnumber)
   # all_.append(trainnumber)
        start=u"出發時間"+str(i.find(class_="column3").text)
        print(start)
  #  all_.append(start)
        arrive=u"到達時間"+str(i.find(class_="column4").text)
        print(arrive)
   # all_.append(arrive)
        #data='{}\n{}\n{}\n{}\n\n'.format(trainnumber,start,arrive)
        data=trainnumber+" "+start+" "+arrive+"\n"
        content+=data
       
    return content


def ptt_beauty():
    rs = requests.session()
    res = rs.get('https://www.ptt.cc/bbs/Beauty/index.html', verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    all_page_url = soup.select('.btn.wide')[1]['href']
    start_page = get_page_number(all_page_url)
    page_term = 2  # crawler count
    push_rate = 10  # 推文
    index_list = []
    article_list = []
    for page in range(start_page, start_page - page_term, -1):
        page_url = 'https://www.ptt.cc/bbs/Beauty/index{}.html'.format(page)
        index_list.append(page_url)

    # 抓取 文章標題 網址 推文數
    while index_list:
        index = index_list.pop(0)
        res = rs.get(index, verify=False)
        # 如網頁忙線中,則先將網頁加入 index_list 並休息1秒後再連接
        if res.status_code != 200:
            index_list.append(index)
            # print u'error_URL:',index
            # time.sleep(1)
        else:
            article_list = craw_page(res, push_rate)
            # print u'OK_URL:', index
            # time.sleep(0.05)

    content = ''
    for article in article_list:
        data = '[{} push] {}\n{}\n\n'.format(article.get('title', None), article.get('title', None),
                                             article.get('url', None))
        content += data
    return content



@handler.add(MessageEvent, message=TextMessage)
def handle_messag(event):
    if event.message.text=="bang":
        num=random.randint(0,len(bang))
        image_message=ImageSendMessage(
            original_content_url=bang[num],
            preview_image_url=bang[num]
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0
    if "高鐵" in event.message.text :
        t=event.message.text
        t=t.split().strip()
        content=tran(t[1],t[2])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "beauty":
        content=ptt_beauty()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "t":
        content=tran()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0

    
    if event.message.text == "beauty1":
        content=beauty()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if "庭宇" in event.message.text:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="???"))
    
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="媽的徐胤桓智障"))
        return 0

    buttons_template = TemplateSendMessage(
        alt_text='目錄 template',
        template=ButtonsTemplate(
            title='選擇服務',
            text='請選擇',
            thumbnail_image_url='https://i.imgur.com/kzi5kKy.jpg',
            actions=[
                MessageTemplateAction(
                    label='開始玩',
                    text='開始玩'
                ),
                URITemplateAction(
                    label='影片介紹 阿肥bot',
                    uri='https://youtu.be/1IxtWgWxtlE'
                ),
                URITemplateAction(
                    label='如何建立自己的 Line Bot',
                    uri='https://github.com/twtrubiks/line-bot-tutorial'
                ),
                URITemplateAction(
                    label='聯絡作者',
                    uri='https://www.facebook.com/TWTRubiks?ref=bookmarks'
                )
            ]
        )
    )
    line_bot_api.reply_message(event.reply_token, buttons_template)
if __name__ == "__main__":
    app.run()
