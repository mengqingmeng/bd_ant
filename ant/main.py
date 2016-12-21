# -*- coding: UTF-8 -*-
'''
Created on 2016年8月17日

@author: MQM
'''
import urllib,json,time,codecs,threading
from ant import request
#import requestData
ISOTIMEFORMAT='%Y-%m-%d %X'
print("begin",time.strftime( ISOTIMEFORMAT, time.localtime() ))

ts = []
count = 1000
threads = 100
step = count / threads
for i in range(0, threads):
    #print(int(i*step+1),int((i+1)*step))
    t = threading.Thread(target=request.thread, args=(int(i*step+1),int((i+1)*step),"T" + str(i+1)))
    t.start()
    ts.append(t)

print(len(ts))
for t in ts:
    t.join()

'''
t1 = threading.Thread(target=request.thread, args=(1,250,"T1"))
t2 = threading.Thread(target=request.thread, args=(250,500,"T2"))
t3 = threading.Thread(target=request.thread, args=(500,750,"T3"))
t4 = threading.Thread(target=request.thread, args=(750,1000,"T4"))
t1.start()
t2.start()
t3.start()
t4.start()
t1.join()
t2.join()
t3.join()
t4.join()
'''
# t1 = threading.Thread(target=request.thread, args=(5,20,"main"))
# t1.start()
# t1.join()
print("end",time.strftime( ISOTIMEFORMAT, time.localtime() ))