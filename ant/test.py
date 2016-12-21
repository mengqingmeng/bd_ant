# -*- coding: UTF-8 -*-

from urllib import request
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import mysql.connector,time,threading,logging

lock = threading.Lock()

conn = mysql.connector.connect(user='devep', password='development@hufu', database='gexinghufu')
cursor = conn.cursor()

productName ='欧珀莱臻源心肌系列洁面乳'

baseUrl = 'http://www.baidu.com/s'
for page in range(0,10):
    parameters = {'wd': productName,'pn':str(10*page)}
    baseUrl = '{}?{}'.format(baseUrl, urlencode(parameters))#将参数编码

    req = request.Request(baseUrl)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
    with request.urlopen(baseUrl) as f:
        data = f.read()
        soup = BeautifulSoup(data, "lxml")

        for result in soup.find_all("div",{"class":"result"}):#查找class="result"的div,保存结果
            cursor.execute('insert into business_product_baidu_info (pid,pname,info) values (%s,%s,%s)',(str(5),str(productName),str(result)))
            conn.commit()

    print("succ--productName:%s,Page:%d" ,productName,page+1)
