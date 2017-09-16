import random
import requests
import re
from bs4 import BeautifulSoup
from flask import Flask,request,abort
#import sys  
#reload(sys)  
#sys.setdefaultencoding('utf-8')


item=['sdf','frfr','ffrf']
if __name__=="__main__":
    num=random.randint(0,len(item))
    print(num,item[num])
