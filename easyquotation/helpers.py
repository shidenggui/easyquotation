# coding:utf8
import json
import os
import re

import requests

STOCK_CODE_PATH = 'stock_codes.conf'


def update_stock_codes():
    """获取所有股票 ID 到 all_stock_code 目录下"""
    all_stock_codes_url = 'http://www.shdjt.com/js/lib/astock.js'
    grep_stock_codes = re.compile('~(\d+)`')
    response = requests.get(all_stock_codes_url)
    all_stock_codes = grep_stock_codes.findall(response.text)
    with open(stock_code_path(), 'w') as f:
        f.write(json.dumps(dict(stock=all_stock_codes)))


def get_stock_codes(realtime=False):
    """获取所有股票 ID 到 all_stock_code 目录下"""
    if realtime:
        all_stock_codes_url = 'http://www.shdjt.com/js/lib/astock.js'
        grep_stock_codes = re.compile('~(\d+)`')
        response = requests.get(all_stock_codes_url)
        stock_codes = grep_stock_codes.findall(response.text)
        with open(stock_code_path(), 'w') as f:
            f.write(json.dumps(dict(stock=stock_codes)))
        return stock_codes
    else:
        with open(stock_code_path()) as f:
            return json.load(f)['stock']


def stock_code_path():
    return os.path.join(os.path.dirname(__file__), STOCK_CODE_PATH)
