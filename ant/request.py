# -*- coding: UTF-8 -*-

from urllib import request
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import mysql.connector,time,threading,logging

conn = mysql.connector.connect(user='root', password='', database='ant_new')
cursor = conn.cursor()

def thread(fromIndex,toIndex):
    for productIndex in range(fromIndex,toIndex):

        baseUrl = 'http://www.baidu.com/s'
        for i in range(0,10):
            parameters = {'wd': '嘉娜宝美白爽肤水','pn':str(10*i)}

            baseUrl = '{}?{}'.format(baseUrl, urlencode(parameters))#将参数编码

            req = request.Request(baseUrl)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
            with request.urlopen(baseUrl) as f:
                data = f.read()
                soup = BeautifulSoup(data, "lxml")
                for result in soup.find_all("div",{"class":"result"}):#查找class="result"的div
                    print(result)
