#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import os
import re
from bs4 import BeautifulSoup

url = 'https://www.mzitu.com/222008'
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:66.0) Gecko/20100101 Firefox/66.0",
          "Referer": "https://www.mzitu.com/jiepai/comment-page-1/"
          }

response = requests.get(url, headers=header)  # 请求网页
print(response)
html = response.text
# print(html)
content = response.content  # 获取html


bsobj = BeautifulSoup(content, 'lxml')  # 解析html
title = bsobj.find('h2', class_='main-title').string  # 需要用class_
picture_max = bsobj.find('div', class_='pagenavi').find_all('a')[-2].string  # 一共多少张图

dir_name = re.findall('<h2 class="main-title">(.*?)</h2>', html)[-1]

if not os.path.exists(dir_name):
    os.mkdir(dir_name)

for i in range(1, int(picture_max)):
    print('正在获取{}第{}图片'.format(title, i))
    href = url + '/' + str(i)  # 访问每一页
    response = requests.get(href, headers=header)  # 请求数据
    content = response.content  # 得到二进制对象
    soup = BeautifulSoup(content, 'lxml')  # 初始化

    # 找img标签，访问src属性，找图片url
    picture_url = soup.find('img', alt=title).attrs['src']
    # 访问图片url
    response_img = requests.get(picture_url, headers=header)
    # 获取二进制图片文件
    content_img = response_img.content
    # 命名文件，注意加.jpg
    file_name = title + '-' + str(i) + '.jpg'
    # 写入，注意以二进制写入方式打开
    # with open(dir_name + '/' + file_name, 'wb') as f:
    #     f.write(content_img)
