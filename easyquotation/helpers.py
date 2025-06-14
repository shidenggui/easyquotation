# coding:utf8
import json
import os

import requests
from datetime import datetime
from typing import Optional

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

def tencent_quote(stock):
    def _safe_float(s: str) -> Optional[float]:
        try:
            return float(s)
        except ValueError:
            return None

    def _safe_acquire_float(stock: list, idx: int) -> Optional[float]:
        """
        There are some securities that only have 50 fields. See example below:
        ['\nv_sh518801="1',
        '国泰申赎',
        '518801',
        '2.229',
        ......
         '', '0.000', '2.452', '2.006', '"']
        """
        try:
            return _safe_float(stock[idx])
        except IndexError:
            return None

    return {
        "name": stock[1],
        "code": stock[2],
        "now": float(stock[3]),
        "lclose": float(stock[4]),
        "open": float(stock[5]),
        "volume": float(stock[6]) * 100,
        "bid_volume": int(stock[7]) * 100,
        "ask_volume": float(stock[8]) * 100,
        "bid1": float(stock[9]),
        "bid1_volume": int(stock[10]) * 100,
        "bid2": float(stock[11]),
        "bid2_volume": int(stock[12]) * 100,
        "bid3": float(stock[13]),
        "bid3_volume": int(stock[14]) * 100,
        "bid4": float(stock[15]),
        "bid4_volume": int(stock[16]) * 100,
        "bid5": float(stock[17]),
        "bid5_volume": int(stock[18]) * 100,
        "ask1": float(stock[19]),
        "ask1_volume": int(stock[20]) * 100,
        "ask2": float(stock[21]),
        "ask2_volume": int(stock[22]) * 100,
        "ask3": float(stock[23]),
        "ask3_volume": int(stock[24]) * 100,
        "ask4": float(stock[25]),
        "ask4_volume": int(stock[26]) * 100,
        "ask5": float(stock[27]),
        "ask5_volume": int(stock[28]) * 100,
        "最近逐笔成交": stock[29],
        "datetime": datetime.strptime(stock[30], "%Y%m%d%H%M%S"),
        "涨跌": float(stock[31]),
        "涨跌(%)": float(stock[32]),
        "high": float(stock[33]),
        "low": float(stock[34]),
        "价格/成交量(手)/成交额": stock[35],
        "成交量(手)": int(stock[36]) * 100,
        "成交额(万)": float(stock[37]) * 10000,
        "turnover": _safe_float(stock[38]),
        "PE": _safe_float(stock[39]),
        "unknown": stock[40],
        "high_2": float(stock[41]),  # 意义不明
        "low_2": float(stock[42]),  # 意义不明
        "振幅": float(stock[43]),
        "流通市值": _safe_float(stock[44]),
        "总市值": _safe_float(stock[45]),
        "PB": float(stock[46]),
        "涨停价": float(stock[47]),
        "跌停价": float(stock[48]),
        "量比": _safe_float(stock[49]),
        "委差": _safe_acquire_float(stock, 50),
        "均价": _safe_acquire_float(stock, 51),
        "市盈(动)": _safe_acquire_float(stock, 52),
        "市盈(静)": _safe_acquire_float(stock, 53),
    }
