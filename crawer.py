#!/usr/bin/python
#coding:utf-8
import random
import requests
import re
from bs4 import BeautifulSoup
from flask import Flask,request,abort
#import sys  
#reload(sys)  
#sys.setdefaultencoding('utf-8')
def eyny_movie():
    target_url = 'http://www.eyny.com/forum-205-1.html'
    print('Start parsing eynyMovie....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ''
    for titleURL in soup.select('.bm_c tbody .xst'):
        title = titleURL.text.encode('utf-8')
        if '11379780-1-3' in titleURL['href']:
            continue
        if '台' in title:
            link = 'http://www.eyny.com/' + titleURL['href']
            data = '{}\n{}\n\n'.format(title, link)
            content += data
    return content




item=['sdf','frfr','ffrf']
if __name__=="__main__":
  #  num=random.randint(0,len(item))
  print(eyny_movie())
   # print(num,item[num])
