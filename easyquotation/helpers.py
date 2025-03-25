# coding:utf8
import json
import os
import re

import requests

STOCK_CODE_PATH = os.path.join(os.path.dirname(__file__), "stock_codes.conf")


def update_stock_codes():
    """更新内置股票代码表"""
    response = requests.get("https://shidenggui.com/easy/stock_codes.json", headers ={'Accept-Encoding':'gzip'})
    with open(STOCK_CODE_PATH, "w") as f:
        f.write(response.text)
    return response.json()


def get_stock_codes(realtime=False):
    """获取内置股票代码表
    :param realtime: 是否获取实时数据, 默认为否"""
    if realtime:
        return update_stock_codes()
    with open(STOCK_CODE_PATH) as f:
        return json.load(f)["stock"]


def get_stock_type(stock_code):
    """判断股票ID对应的证券市场
    匹配规则
    ['4'， '8'] 为 bj
    ['5', '6', '7', '9', '110', '113', '118', '132', '204'] 为 sh
    其余为 sz
    :param stock_code:股票ID, 若以 'sz', 'sh', 'bj' 开头直接返回对应类型，否则使用内置规则判断
    :return 'bj', 'sh' or 'sz'"""
    assert isinstance(stock_code, str), "stock code need str type"
    bj_head = ("43", "83", "87", "92")
    sh_head = ("5", "6", "7", "9", "110", "113", "118", "132", "204")
    if stock_code.startswith(("sh", "sz", "zz", "bj")):
        return stock_code[:2]
    elif stock_code.startswith(bj_head):
        return "bj"
    elif stock_code.startswith(sh_head):
        return "sh"
    return "sz"
