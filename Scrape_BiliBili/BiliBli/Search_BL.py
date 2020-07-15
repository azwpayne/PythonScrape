import requests
from parsel import Selector
import random
import time

# URL = 'https://search.bilibili.com/all?keyword=python&page={page}'

keyword = input("请输入所需查询的关键字： ")
URL = f'https://search.bilibili.com/all?keyword={keyword}'

header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',

}


def scrape(url):
    try:
        print("Scraping URL:  %s ..." % url)
        response = requests.get(url=url, headers=header)
        # 查看是否被反爬
        print(response.text[500:2000])
        # 添加随机睡眠，规避请求过快造成封IP
        time.sleep(random.random() + 1)
        if response.status_code == 200:
            return response.text
        else:
            pass
    except Exception as e:
        print(e)


def scrape_list(page):
    url = f'{URL}/&page={page}'
    return scrape(url)


def parse(text):
    selector = Selector(text)
    data = selector.css("#all-list  .video-list .info")
    # item = {}
    for i in data:
        title = i.css(".title ::attr(title)").extract_first()
        href = i.css(".title ::attr(href)").extract_first()
        heat = i.css(".tags ::text").extract_first().strip()
        upload = i.css(".so-icon.time ::text").extract_first().strip()
        info = f'{title},{heat},{upload}, https:{href}\n'
        print(info)
        # save(info)


def save(info):
    with open('Search_BL.csv', 'a+', encoding='utf-8') as f:
        f.write(info)


def main(page):
    text = scrape_list(page=page)
    parse(text)


if __name__ == '__main__':
    [main(page=page) for page in range(1, 10)]
