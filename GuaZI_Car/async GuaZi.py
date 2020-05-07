# -*- coding: utf-8 -*-
# @Time     :   2020/5/7 13:51
# @Author   :   Payne
# @File     :   async GuaZi.py
# @Software :   PyCharm

import asyncio
import json
import time
from pyquery import PyQuery as pq
import aiohttp
import logging
from aiohttp import ContentTypeError
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

CONCURRENCY = 5


class Spider(object):

    def __init__(self):
        self.semaphore = asyncio.Semaphore(CONCURRENCY)
        self.header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'antipas=0977e68008933398852413u7; uuid=f2d73672-5570-405b-ae46-6d437560eb56; cityDomain=cs; clueSourceCode=%2A%2300; user_city_id=204; preTime=%7B%22last%22%3A1588811748%2C%22this%22%3A1588811748%2C%22pre%22%3A1588811748%7D; ganji_uuid=3245948171553910526688; cainfo=%7B%22ca_a%22%3A%22-%22%2C%22ca_b%22%3A%22-%22%2C%22ca_s%22%3A%22self%22%2C%22ca_n%22%3A%22self%22%2C%22ca_medium%22%3A%22-%22%2C%22ca_term%22%3A%22-%22%2C%22ca_content%22%3A%22-%22%2C%22ca_campaign%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22scode%22%3A%22-%22%2C%22keyword%22%3A%22-%22%2C%22ca_keywordid%22%3A%22-%22%2C%22display_finance_flag%22%3A%22-%22%2C%22platform%22%3A%221%22%2C%22version%22%3A1%2C%22client_ab%22%3A%22-%22%2C%22guid%22%3A%22f2d73672-5570-405b-ae46-6d437560eb56%22%2C%22ca_city%22%3A%22xiangtan%22%7D; sessionid=c2a93c8e-71ec-4396-ffcc-167a04d7dd17; lg=1',
            'DNT': '1',
            'Host': 'www.guazi.com',
            'Pragma': 'no-cache',
            'Referer': 'https://www.guazi.com/cs/buy/o1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
        }

    async def scrape(self, url):
        async with self.semaphore:
            async with aiohttp.ClientSession(headers=self.header).get(url) as response:
                await asyncio.sleep(1)
                return await response.text()

    async def scrape_index(self, page):
        url = f'https://www.guazi.com/cs/buy/o{page}/#bread'
        html = await self.scrape(url)
        await self.parse(html)

    async def parse(self, html):
        with open('car.csv', 'a+', encoding='utf-8') as f:
            doc = pq(html)
            for message in doc('body > div.list-wrap.js-post > ul > li > a').items():
                # 汽车简介
                car_name = message('h2.t').text()
                # 汽车详情(年限、里程、服务)
                car_info = message('div.t-i').text()
                year = car_info[:5]
                mileage = car_info[6:-5]
                service = car_info[13:].replace('|', '')
                # 价格
                try:
                    price = message('div.t-price > p').text()
                except AttributeError:
                    price = message('em.line-through').text()
                car_pic = message('img').attr('src')
                data = f'{car_name}, {year},{mileage}, {service}, {price}\n'
                logging.info(data)
                f.write(data)

    async def main(self):
        scrape_index_tasks = [asyncio.ensure_future(self.scrape_index(page)) for page in range(51)]
        await asyncio.gather(*scrape_index_tasks)


if __name__ == '__main__':
    spider = Spider()
    asyncio.get_event_loop().run_until_complete(spider.main())
