# -*- coding: utf-8 -*-
# @Time     :   2020/4/3 0:40
# @Author   :   Payne
# @File     :   Girl Figure.py
# @Software :   PyCharm
import multiprocessing
import os
import random
import re
import time
from urllib.parse import urljoin
import requests
from pyquery import PyQuery as pq
import logging
from requests import ReadTimeout, HTTPError, ConnectionError
from fake_useragent import UserAgent

BASE_URL = 'https://www.mzitu.com'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


def User_Agent(page):
    User_Agent = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
    ]
    this_ua = random.choice(User_Agent)
    global header
    header = {"User-Agent": this_ua,
              'Referer': f'https://www.mzitu.com/page/{page}/'}
    # return header


def scrape_page(url):
    logging.info('scraping %s...', url)
    # header = User_Agent(page)
    # print(header)
    try:
        response = requests.get(url, headers=header)
        return response.text
    except TimeoutError as a:
        logging.error(f"Error time is Out:{a}")
    except ReadTimeout as b:
        logging.error(f"Error ReadTimeout: {b}")
    except HTTPError as c:
        logging.error(f"Error HTTPError: {c}")
    except ConnectionError as d:
        logging.error(f"Error ConnectionError: {d}")


def scrape_index(page):
    index_url = f"{BASE_URL}/page/{page}/"
    return scrape_page(index_url)


def parse_index(html):
    doc = pq(html)
    # links = doc('.postlist #pins li [target="_blank"]')
    links = doc('.postlist #pins > li > span:nth-child(2) > a')
    for link in links.items():
        detail_url = link.attr('href')
        logging.info('Got detail_url %s', detail_url)
        yield detail_url


def scrape_detail(url):
    return scrape_page(url)


def parse_detail_index(html):
    doc = pq(html)
    picture_max = doc('body > div.main > div.content > div.pagenavi > a:nth-child(7) > span').text()
    global title
    title = doc('.main .content .main-title').text()
    return int(picture_max)
    # title = soup.find('h2', class_='main-title').string  # 需要用class_
    # picture_max = soup.find('div', class_='pagenavi').find_all('a')[-2].string  # 一共多少张图
    # dir_name = re.findall('<h2 class="main-title">(.*?)</h2>', html1)[-1]
    # if not os.path.exists(dir_name):
    #     os.mkdir(dir_name)
    # return int(picture_max)


def scrape_detail_page(detail_url, page):
    picture_url = f"{detail_url}/{page}"
    html = scrape_page(picture_url)
    doc = pq(html)
    picture_uris = doc('body > div.main > div.content > div.main-image > p > a > img')
    for picture_uri in picture_uris:
        try:
            src = picture_uris.attr('src')
            if src:
                logging.info(f'The Picture_url {src}...', )
                return src
        except Exception as e:
            print(e)

    # for picture_url in picture_urls:
    #     href = picture_urls.attr('href')
    #     print(href)
    # return scrape_page(picture_url)


def scrape_picture(url, page):
    response = requests.get(url, headers=header).content
    # 获取二进制图片文件
    # content_img = resp_img.content
    # # 命名文件，注意加.jpg
    file_name = title + '-' + str(page) + '.jpg'
    item = title + '/' + file_name
    logging.info(f'Successfully acquired: {file_name}')
    with open(item, 'wb+')as f:
        f.write(response)


def main(page):
    User_Agent(page)
    index_html = scrape_index(page)
    detail_urls = parse_index(index_html)
    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)
        global picture_max
        picture_max = parse_detail_index(detail_html)
        print(title)
        if not os.path.exists(title):
            os.mkdir(title)
        for a in range(1, picture_max+1):
            picture_url = scrape_detail_page(detail_url, a)
            scrape_picture(picture_url, a)
            time.sleep(3)


if __name__ == '__main__':
    for page in range(1, 2):
        main(page)
    time.sleep(3)
# if __name__ == '__main__':
#     pool = multiprocessing.Pool()
#     pages = range(1, 3 + 1)
#     pool.map(main, pages)
#     pool.close()
