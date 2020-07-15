import logging
import random
import requests
import re
from parsel import Selector

# header = {
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
#     'cache-control': 'max-age=0',
#     'dnt': '1',
#     'sec-fetch-dest': 'document',
#     'sec-fetch-mode': 'navigate',
#     'sec-fetch-site': 'none',
#     'sec-fetch-user': '?1',
#     'upgrade-insecure-requests': '1',
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
#
# }
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')


# 定义用户请求头
def ua():
    ua = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    ]
    Ua = random.choice(ua)
    header = {"User-Agent": Ua,
              'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
              'accept-encoding': 'gzip, deflate, br',
              'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
              'cache-control': 'max-age=0',
              'dnt': '1',
              'sec-fetch-dest': 'document',
              'sec-fetch-mode': 'navigate',
              'sec-fetch-site': 'none',
              'sec-fetch-user': '?1',
              'upgrade-insecure-requests': '1'

              }
    return header


# 定义爬取方法
def scrap_page(url):
    try:
        header = ua()
        response = requests.get(url, headers=header)
        UseHeader = ua()['User-Agent']
        logging.info(f"Using header {UseHeader}")
        if response.status_code == 200:
            return response.content.decode('utf-8')
        logging.error(f'get invalid status code {response.status_code} while scraping {url}')
    except requests.RequestException:
        logging.error('error occurred while scraping %s', url, exc_info=True)


#  定义获取弹幕url所需所需参数oid方法
def get_oid(URL):
    text = scrap_page(URL)
    # print(text)
    cid = re.findall('.*?cid":+(\d{9})+', text)[0]
    logging.info(f"The CID :{cid}")
    return cid


# 爬取弹幕页
def scrape_index(cid):
    Barrage_url = f'https://api.bilibili.com/x/v1/dm/list.so?oid={cid}'
    return scrap_page(Barrage_url)

# 解析弹幕页
def parse(Barrage):
    selector = Selector(Barrage)
    data = selector.xpath('//d/text()').extract()
    for i in data:
        messages = f'{i}\n'
        save_data(messages)


def save_data(data):
    with open("Barrage.txt", 'a+', encoding='utf-8') as f:
        f.write(data)


def main():
    URL = 'https://m.bilibili.com/video/BV1jT4y1J77v'
    cid = get_oid(URL)
    Barrage = scrape_index(cid)
    parse(Barrage)


if __name__ == '__main__':
    main()
