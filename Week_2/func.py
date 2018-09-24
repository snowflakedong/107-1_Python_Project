from bs4 import BeautifulSoup as bs
from urllib.parse import quote
import pandas as pd
import numpy as np
import requests
import time

### 詳細過程可以參考外部的檔案，函式內容與檔名相同

def getUrls():
    url = 'http://e-service.cwb.gov.tw/HistoryDataQuery/QueryDataController.do?command=viewMain&_=1528379589863'
    html = requests.get(url)
    soup = bs(html.text, 'html.parser')
    script = soup.select('script')[2]
    string = str(script)
    area = pick(string, 'var stList = {', '}')
    split = area.split(sep='\"')
    url = 'https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station='
    areaCity = []
    areaTW = []
    areaEng = []
    areaUrl = []
    for ind in range(1, len(split), 2*4):
        areaCity.append(split[ind+6].strip())
        areaTW.append(split[ind+2].strip())
        areaEng.append(split[ind+4])
        areaUrl.append(url + split[ind] + '&stname=' + '%25'.join(quote(split[ind+2].strip()).split('%')) + '&datepicker=')
    station_info = pd.DataFrame({'City' : areaCity, 'Chinese' : areaTW, 'English' : areaEng, 'Url' : areaUrl})
    return station_info


def getClimate(position, date, info): 
    precipitation = []
    temperature = []    

    if position[0] == '台':
        position = '臺' + position[1:] #台-->臺

    for i in info[info['City']==position].index:  
        
        #time.sleep(0.11)  需要delay才不會被擋
                
        data = pd.read_html(info.loc[i,'Url'] + date)[1].iloc[2:,[3,10]] # 3:temp, 10:precip
            
        temp = pd.to_numeric(data[3], errors = 'coerce', downcast = 'float')
        if temp.count()!=0:
            temperature.append(temp.mean())
        temp = pd.to_numeric(data[10], errors = 'coerce', downcast = 'float')
        if temp.count()!=0:
            precipitation.append(temp.mean())
                  
    return np.average(temperature), np.average(precipitation)


def pick(string, start, end):
    startlen = len(start)
    endlen = len(end)
    string = string[string.find(start) + len(start):]
    string = string[:string.find(end)]
    return string