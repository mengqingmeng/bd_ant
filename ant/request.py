# -*- coding: UTF-8 -*-

from urllib import request
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import mysql.connector,time,threading,logging,socket

#lock = threading.Lock()
socket.setdefaulttimeout(5)

log_dest = "F:\JTPData\\baidu\\"

logging.basicConfig(filename=log_dest+'baidu.log',level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

def thread(fromIndex,toIndex,thread):
    conn = mysql.connector.connect(user='devep', password='development@hufu', database='gexinghufu')
    cursor = conn.cursor()
    for productIndex in range(fromIndex,toIndex):
        cursor.execute('select name from business_skin_note_recommend_product where id = %s',(str(productIndex),))
        productInfo = cursor.fetchall()
        if(not productInfo):#如果该id没有产品信息，打印日志，继续执行循环
            logging.debug("none--id:%d T:%s" ,productIndex,thread)
            continue
        productName = productInfo[0][0]
        baseUrl = 'http://www.baidu.com/s'
        for page in range(0,2):
            cursor.execute('select id from business_product_baidu_info where pid = %s and page = %s', (str(productIndex),str(page+1)))
            infoLine = cursor.fetchall()#info结果
            if(infoLine):#如果数据库里已经有了记录，则跳过
                logging.debug("repeat--pid:%d,Page:%d,T:%s" ,productIndex,page,thread)
                continue
            #没有 就去爬
            parameters = {'wd': productName,'pn':str(10*page)}
            baseUrl = '{}?{}'.format(baseUrl, urlencode(parameters))#将参数编码

            req = request.Request(baseUrl)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36')
            try:
                with request.urlopen(baseUrl) as f:
                    data = f.read()
                    soup = BeautifulSoup(data, "lxml")

                    for result in soup.find_all("div",{"class":"result"}):#查找class="result"的div,保存结果
                        try:
                            cursor.execute('insert into business_product_baidu_info (pid,pname,page,info) values (%s,%s,%s,%s)',(str(productIndex),str(productName),str(page+1),str(result)))
                            conn.commit()
                        except:
                            logging.debug("fail--Pid:%d,Page:%d,T:%s" ,productIndex,page+1,thread)
            except:
                logging.debug("netError-Pid:%d,Page:%d,T:%s" ,productIndex,page+1,thread)
            logging.debug("succ--Pid:%d,Page:%d,T:%s" ,productIndex,page+1,thread)