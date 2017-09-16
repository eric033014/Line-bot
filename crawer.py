import requests
import re
from bs4 import BeautifulSoup
from flask import Flask,request,abort
#import sys  
#reload(sys)  
#sys.setdefaultencoding('utf-8')
def crawer():
    target_url = 'http://www.eyny.com/forum-205-1.html'
    rs=requests.get(target_url)
    rs.encoding='utf-8'
    #print(rs.text)
    soup=BeautifulSoup(rs.text,'html.parser')
    content=''
    for i in soup.select('.bm_c tbody .xst'):
        title=i.text.encode('utf-8')
        #print(i.text)
        if '11379780-1-3' in i['href']:
            continue
        link = 'http://ww.eyny.com/'+i['href']
        data = '{}\n{}\n\n'.format(title,link)
        content+=data
    return content
def beauty():
    target_url = 'https://www.ptt.cc/bbs/Beauty/index.html'
    rs=requests.get(target_url)
    rs.encoding='utf-8'
   # print(rs.text)
    soup=BeautifulSoup(rs.text,'html.parser')
    content=''
    for i in soup.select('.r-ent .title'):
        title=i.text.encode('utf-8')
        if i.find('a'):
            #print(i.text)
        #if '11379780-1-3' in i['href']:
        #    continue
            link = 'https://www.ptt.cc'+i.find('a')['href']
            data = '{}\n{}\n\n'.format(title,link)
            content+=data
    return content




if __name__=="__main__":
    content='FRGEG'
    content=beauty()
    print(content)
