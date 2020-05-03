# -*- coding: utf-8 -*-
# @Time     :   2020/3/25 4:48
# @Author   :   Payne
# @File     :   ProperTranslation.py
# @Software :   PyCharm

from time import time, sleep
import random
import hashlib
import requests


def hex5(value):
    manipulator = hashlib.md5()
    manipulator.update(value.encode('utf-8'))
    return manipulator.hexdigest()


def Mach(string):
    e = string
    ts = round(time())
    salt = str(ts) + str(random.randint(0, 9))
    bv = hex5(
        "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36")
    sign = hex5("fanyideskweb" + e + salt + "Nw(nmmbP%A-r6U3EUn]Aj")
    data = {
        'i': e,
        'from': 'AUTO',
        'to': 'AUTO',
        'smartresult': 'dict',
        'client': 'fanyideskweb',
        'salt': salt,  # salt = ts + 一个随机数
        'sign': sign,
        'ts': ts,  # ts 时间戳
        'bv': bv,
        'doctype': 'json',
        'version': '2.1',
        'keyfrom': 'fanyi.web',
        'action': 'FY_BY_REALTlME',
    }
    return data


def Translation(url, data):
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '237',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'OUTFOX_SEARCH_USER_ID=1648504734@10.169.0.83; OUTFOX_SEARCH_USER_ID_NCOO=1054516127.1065001; JSESSIONID=aaaFtapMs3Ow4bIaK06-w; ___rl__test__cookies=1580462241081',
        'DNT': '1',
        'Host': 'fanyi.youdao.com',
        'Origin': 'https://fanyi.youdao.com',
        'Referer': 'https://fanyi.youdao.com/',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    response = requests.post(url, headers=header, data=data)
    return response


def main():
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    e = input('请输需翻译的内容（不得大于5000字！）:')
    data = Mach(e)
    translate = Translation(url, data=data)
    print(translate.json()['translateResult'][0][0]['tgt'])


if __name__ == '__main__':
    while True:
        main()
