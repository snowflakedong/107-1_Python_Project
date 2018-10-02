from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import requests
import time
import re

### 詳細過程可以 Week_2 範例

def getCPI(date):
    yy = int(date[0:4])
    mm = int(date[-2:])
    if len(date)==7:
        yy -= 1911
    page = 1
    year = []
    month = []
    CPI = []
    WPI = []
    end = 1
    while(end):
        url = 'https://www.stat.gov.tw/lp.asp?CtNode=489&CtUnit=1818&BaseDSD=29&nowPage=' + str(page) + '&pagesize=25'
        html = requests.get(url)
        soup = bs(html.text, 'html.parser')
        text = soup.find_all('a', title=re.compile("CPI|WPI"))
        for i in range(len(text)):
            temp = re.split('年|月|增率|，|％', text[i].string)
            year.append(int(temp[0]))
            month.append(int(temp[1]))
            CPI.append(temp[4][1:] if temp[4][0]=='漲' else '-'+temp[4][1:])
            WPI.append(temp[-2][1:] if temp[-2][0]=='漲' else '-'+temp[-2][1:])
            if((year[-1]==yy)&(month[-1]==mm)):
                end = 0
                break
        page += 1
    return pd.DataFrame({'Year' : year, 'Month' : month, 'CPI (%)': CPI, 'WPI (%)' : WPI})\
            [['Year', 'Month', 'CPI (%)', 'WPI (%)']]
