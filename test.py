
# -*- coding: utf8 -*-

#!/usr/bin/python
#encoding:utf-8

import urllib
from bs4 import BeautifulSoup
url = "http://www.thsrc.com.tw/tw/TimeTable/SearchResult"
request = urllib.request.Request(url) 
request.add_header("User-Agent","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36")

form_data = {
    "StartStation": "977abb69-413a-4ccf-a109-0272c24fd490", 
    "EndStation": "f2519629-5973-4d08-913b-479cce78a356",
    "SearchDate": "2017/10/24",
    "SearchTime": "17:00",
    "SearchWay":"DepartureInMandarin",
    "RestTime":"",
    "EarlyOrLater":""
}
print(form_data["StartStation"])
form_data = urllib.parse.urlencode(form_data).encode("utf-8")
response = urllib.request.urlopen(request,data=form_data)  
html = response.read()
soup= BeautifulSoup(html, 'html.parser')
all_=[]
for i in soup.find_all(class_="touch_table"):
    t=u"車次"
    trainnumber=t+i.find(class_="column1").text
    print(trainnumber)
   # all_.append(trainnumber)
    start=u"出發時間"+i.find(class_="column3").text
    print(start)
  #  all_.append(start)
    arrive=u"到達時間"+i.find(class_="column4").text
    print(arrive)
   # all_.append(arrive)
    all_.append({u"車次":trainnumber,u"起站":start,u"終點":arrive})
print(all_)
#file_out = file("02_thsrc.html",'w')
#file_out.write(html)
#file_out.close()
#print (html)
