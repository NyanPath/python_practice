#-*- coding: UTF-8 -*-
from selenium import webdriver
import time
import re
import random
import xlrd, xlwt

def getPrice(html):
    # 获取商品价格
    reg = r'strong>(.+?)</strong'
    price_list = re.findall(re.compile(reg), html)
    return price_list


def getSeals(html):
    # 获取销量
    reg = r'deal-cnt">(\d+).*?</div'
    seals_list = re.findall(re.compile(reg), html)
    return seals_list


def getName(html):
    # 商品名称
    reg = r'raw_title":"(.+?)",'
    name_list = re.findall(re.compile(reg), html)
    return name_list


def getLink(html):
    # 商品链接
    reg = r' href="(.+?)" data-nid'
    link_list = re.findall(re.compile(reg), html)
    return link_list
browser = webdriver.Firefox()
browser.get("https://www.taobao.com/")
# 跳过指引
try:
    browser.find_element_by_class_name("xsyd2-close").click()
except:
    pass

# 开始搜索
keyWord = 'vr一体机'  # 关键词
browser.find_element_by_id('q').send_keys(keyWord.decode('utf-8'))  # 输入关键词
time.sleep(2)
browser.find_element_by_class_name("btn-search").click()  # 点击搜索
workbook = xlwt.Workbook()
row = 1
sheet1 = workbook.add_sheet(keyWord.decode('utf-8'), cell_overwrite_ok=True)
for page in range(24, 51):
    html = browser.page_source  # 获取源码
    # 结果数据存入数组
    price_list = getPrice(html)
    p = len(price_list)
    seals_list = getSeals(html)
    s = len(seals_list)
    name_list = getName(html)
    n = len(name_list)
    link_list = getLink(html)
    l = len(link_list)
    # 结果数据写入
    if p > s:
        temp = s
    else:
        temp = p
    if n > temp:
        if temp < l:
            pass
    else:
        temp = n
        if temp > l:
            temp = l
    for item in range(1, int(temp)):
        # 写入名称
        name = name_list[item]
        sheet1.write(row, 1, name)
        # 写入价格
        try:
            price = price_list[item].encode('utf-8')
            sheet1.write(row, 2, price.decode('utf-8'))
        except IndexError:
            pass
        # 写入销量
        seals = seals_list[item].encode('utf-8')
        sheet1.write(row, 3, seals.decode('utf-8'))
        # 写入链接
        links = link_list[item].encode('utf-8')
        sheet1.write(row, 4, links.decode('utf-8'))
        row += 1
    page += 1
    browser.find_element_by_class_name("icon-btn-next-2").click()  # 点击下一页
    delay = random.randint(5, 10)
    time.sleep(int(delay))

workbook.save(keyWord.decode('utf-8').encode('gbk') + '.xls')
