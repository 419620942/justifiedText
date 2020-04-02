#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import database
#可以使用的url
list=[15335287,13495332,12438452,10167348,7704150,15081291,13754755,13754608,15230833]
#不可以使用的url
ll=[20960386,10050485,9848063,10595949,10771117,9987189,21639667,21403332]
#http://www.edewakaru.com/archives/15335287.html

def spaide(id):
    url = 'http://www.edewakaru.com/archives/{}.html'.format(id)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    res = requests.get(url, headers=headers, timeout=10).text
    soup = BeautifulSoup(res, 'lxml')
    data = soup.select('#main-inner > article > div > div')
    p = re.findall('</a><br/>【(.*?)<img ', str(data[0]), re.S)
    YUFA = database.TYUFA()
    YUFA.YUFA = soup.title
    if len(p) == 0:
        p = re.findall('</a><br/><br/>【(.*?)<img ', str(data[0]), re.S)
    #if '［意味］' in p[0]:
    if '【意味】' in p[0]:
        p = p[0].split('<br/>［')
    else:
        p=p[0].replace('【「','「')
        p = p.split('<br/>【')
    for i in p:
        if i[0:2] == '接続':
            ##print('【接続】')
            d = i.split('<br/>')
            JIEXU = []
            for d1 in d[1:-1]:
                d1 = d1.strip()
                if len(d1)>0:
                    JIEXU.append(d1)
            YUFA.JIEXU = '######'.join(str(i) for i in JIEXU)
            ##print('yufajie==='.join(YUFA.JIEXU))
        if i[0:2] == '意味':
            ##print('【意味】')
            d = i.split('<br/>')
            if len(res) != 0:
                d = d[1:-1]
            else:
                d = d[1:-2]
            YISI = []
            for d1 in d:
                p = BeautifulSoup(d1, 'lxml')
                YISI.append(p.get_text())
                ##print(p.get_text())
            YUFA.YISI = '######'.join(str(i) for i in YISI)
        if i[0:2] == '例文':
            ##print('Dasdasdasdasd【例文】')
            d = i.split('<br/><br/>')
            for d1 in d[:-1]:
                if d.index(d1) == 0: d1 = d1[3:]
                p = BeautifulSoup(d1, 'lxml')
                p = p.get_text().split('→')
                YUFA.LIJU.append(p[0])
                ##print(p[0])
                if len(p) >= 2:
                    p1 = p[1].split('（復習')
                    if len(p1) >= 2:
                        ##print('→' + p1[0])
                        for p2 in p1[1:]:
                            YUFA.LIJU.append(p2)
                            ##print('（復習' + p2)
                    else:
                        YUFA.LIJU.append(p1[0])
                        ##print('→' + p1[0])
                ##print()
        if i[0:2] == '説明':
            ##print('【説明】')
            d = i.split('<br/>')
            SHUOMING=[]
            for d1 in d[1:]:
                # if d1!='':
                p = BeautifulSoup(d1, 'lxml')
                SHUOMING.append(p.get_text())
                ##print(p.get_text())
            YUFA.SHUOMING =  '######'.join(str(i) for i in SHUOMING)
                
        ##print()
        return YUFA
#i=input('请输入id:')
print('start...........')
conn = database.opendb('yufa.sqlite')
f = open("yufaid.txt","r")
ids = f.readlines()
for id in ids:
    try:
        yufa = spaide(int(id))
        database.insert_into_T_YUFA(conn,yufa)
        for l in yufa.LIJU:
            lijuObj = database.toTYUFA_LIJU(l)
            database.insert_into_T_SENTENCE(conn,l)
        break
    except:
        print(str(id))
print('end...........')