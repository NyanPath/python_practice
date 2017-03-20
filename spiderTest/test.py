# -*- coding: UTF-8 -*-
import datetime, functools, os, shutil, time, threading, requests, re
from pymongo import MongoClient
from multiprocessing.dummy import Pool as ThreadingPool
from PIL import Image
# class a():
#     def log(func):
#         @ functools.wraps(func)
#         def wrapper(*args, **kw):
#             print 'begin: %s()' % func.__name__
#             func(*args, **kw)
#             print 'end: %s()' % func.__name__
#         return wrapper
#
#
#     @ log
#     def now():
#         print datetime.datetime.now()
#
#     client = MongoClient('localhost', 27017)
#     db = client.Weibo
#     collection = db.user_5829820025
#     a = collection.find()
#     with open('b.txt', 'w') as f:
#         for aaa in a:
#             f.write(aaa['content'] + '\n')
#     f.close
# 新线程执行的代码:
# def loop():
#     print 'thread %s is running...' % threading.current_thread().name
#     n = 0
#     while n < 5:
#         n = n + 1
#         print 'thread %s >>> %s' % (threading.current_thread().name, n)
#         time.sleep(1)
#     print 'thread %s ended.' % threading.current_thread().name
# a = u'呵呵'
# print a
# print 'thread %s is running...' % threading.current_thread().name
# t = threading.Thread(target=loop, name='LoopThread')
# t.start()
# t.join()
# print 'thread %s ended.' % threading.current_thread().name
client = MongoClient('localhost', 27017)
db = client.Proxy
collection = db.Ip
def test(ip):
    try:
        html = requests.get('http://www.bilibili.com/video/part-twoelement-1.html#!page=1', proxies={'http':'http:%s' %ip['proxy']},
                           headers={'User-Agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1Safari/534.50'},
                            timeout=20).content
        if html.find('哔哩哔哩') > 0:
            print 'ip:%s有效' %str(ip['proxy'])
            collection.update({'proxy':ip['proxy']}, {'$set':{'canVisit':'bilibili'}})
        return True
    except Exception:
        print 'ip:%s无法访问bookbao' %str(ip['proxy'])
        collection.update({'proxy': ip['proxy']}, {'$set': {'canVisit': '7kk'}})
    time.sleep(2)

def main():
    ip_list = collection.find()
    pool = ThreadingPool(4)
    pool.map(test, ip_list)
    pool.close()
    pool.join()
main()

def img_resize():
    img_path = 'C:/Users/Administrator/Desktop/新建文件夹 (2)/a.jpg'
    img = Image.open(img_path.decode('utf-8').encode('gbk'))
    img_width = img.size[0]
    img_height = img.size[1]
    small_num = min(img_height,img_width) / 150
    resized_img = img.resize((img_width/small_num, img_height/small_num))
    img_type = img_path.split('/')[-1].split('.')[-1]
    save_path = re.sub(r'\.%s' % img_type, '_new.%s' % img_type, img_path)
    resized_img.save(save_path.decode('utf-8').encode('gbk'))

