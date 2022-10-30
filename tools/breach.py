#!/usr/bin/env python3
import redis
import os
from ransomlook.default import get_socket_path, get_config
from bs4 import BeautifulSoup
import requests
import json

url = 'https://leak-lookup.com/breaches/stats'
source = 'https://leak-lookup.com/breaches'

list_div=[]
red = redis.Redis(unix_socket_path=get_socket_path('cache'), db=4)
res = requests.get(source)
soup=BeautifulSoup(res.text,'html.parser')
divs_name=soup.find('table', {"id": "datatables-indexed-breaches"})
tbody = divs_name.find('tbody')
trs = tbody.find_all('tr')
for tr in trs:
  tds= tr.find_all('td')
  data = tds[3].div.div.a['data-id']
  x = requests.post(url, data={'id':data})
  datas=x.json()
  fields = BeautifulSoup(datas['columns'],'html.parser')
  spans = fields.find_all('span')
  columns=[]
  for span in spans:
      columns.append(span.text.strip())
  datas['columns']=columns
  datas['meta']=''
  datas['location']=[]
  red.set(datas['name'],json.dumps(datas))
print('done')
