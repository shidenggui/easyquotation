import asyncio
import json
from datetime import datetime

import aiohttp

from . import helpers

'''
    '0:      代码
    '1:      名字
    '2:      代码
    '3:      当前价格
    '4:      昨收
    '5:      今开
    '6:      成交量 (手)
    '7:      外盘
    '8:      内盘
    '9:      买一
    '10:     买一量 (手)
    '11-18:  买二 买五
    '19:     卖一
    '20:     卖一量
    '21-28:  卖二 卖五
    '29:     最近逐笔成交
    '30:     时间
    '31:     涨跌
    '32:     涨跌%
    '33:     最高
    '34:     最低
    '35:     价格/成交量（手）/成交额
    '36:     成交量 (手)
    '37:     成交额 (万)
    '38:     换手率
    '39:     市盈率
    '40:
    '41:     最高
    '42:     最低stock_item
    '43:     振幅
    '44:     流通市值
    '45:     总市值
    '46:     市净率
    '47:     涨停价
    '48:     跌停价
'''


class Tencent:
    """腾讯免费行情获取"""

    def __init__(self):
        self.tencent_stock_api = 'http://qt.gtimg.cn/q='
        self.stock_data = []
        self.stock_codes = []
        self.stock_with_exchange_list = []
        self.max_num = 60
        self.load_stock_codes()

        self.stock_with_exchange_list = list(
                map(lambda stock_code: ('sh%s' if stock_code.startswith(('5', '6', '9')) else 'sz%s') % stock_code,
                    self.stock_codes))

        self.stock_list = []
        self.request_num = len(self.stock_with_exchange_list) // self.max_num + 1
        for range_start in range(self.request_num):
            num_start = self.max_num * range_start
            num_end = self.max_num * (range_start + 1)
            request_list = ','.join(self.stock_with_exchange_list[num_start:num_end])
            self.stock_list.append(request_list)

    def load_stock_codes(self):
        with open(helpers.stock_code_path()) as f:
            self.stock_codes = json.load(f)['stock']

    @property
    def all(self):
        return self.get_stock_data()

    async def get_stocks_by_range(self, index):
        print('start', index)
        async with aiohttp.get(self.tencent_stock_api + self.stock_list[index]) as r:
            response_text = await r.text()
            print('end', index)
            self.stock_data.append(response_text)

    def get_stock_data(self):
        del self.stock_data[:]
        threads = []
        for index in range(self.request_num):
            threads.append(self.get_stocks_by_range(index))
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.wait(threads))

        return self.format_response_data()

    def format_response_data(self):
        stocks_detail = ''.join(self.stock_data)
        stock_details = stocks_detail.split(';')
        stock_dict = dict()
        for stock_detail in stock_details:
            stock = stock_detail.split('~')
            if len(stock) <= 49:
                continue
            stock_dict[stock[2]] = {
                'name': stock[1],
                'code': stock[2],
                'now': float(stock[3]),
                'close': float(stock[4]),
                'open': float(stock[5]),
                'volume': float(stock[6]) * 100,
                'bid_volume': int(stock[7]) * 100,
                'ask_volume': float(stock[8]) * 100,
                'bid1': float(stock[9]),
                'bid1_volume': int(stock[10]) * 100,
                'bid2': float(stock[11]),
                'bid2_volume': int(stock[12]) * 100,
                'bid3': float(stock[13]),
                'bid3_volume': int(stock[14]) * 100,
                'bid4': float(stock[15]),
                'bid4_volume': int(stock[16]) * 100,
                'bid5': float(stock[17]),
                'bid5_volume': int(stock[18]) * 100,
                'ask1': float(stock[19]),
                'ask1_volume': int(stock[20]) * 100,
                'ask2': float(stock[21]),
                'ask2_volume': int(stock[22]) * 100,
                'ask3': float(stock[23]),
                'ask3_volume': int(stock[24]) * 100,
                'ask4': float(stock[25]),
                'ask4_volume': int(stock[26]) * 100,
                'ask5': float(stock[27]),
                'ask5_volume': int(stock[28]) * 100,
                '最近逐笔成交': stock[29],  # 换成英文
                'datetime': datetime.strptime(stock[30], '%Y%m%d%H%M%S'),
                '涨跌': float(stock[31]),  # 换成英文
                '涨跌(%)': float(stock[32]),  # 换成英文
                'high': float(stock[33]),
                'low': float(stock[34]),
                '价格/成交量(手)/成交额': stock[35],  # 换成英文
                '成交量(手)': int(stock[36]) * 100,  # 换成英文
                '成交额(万)': float(stock[37]) * 10000,  # 换成英文
                'turnover': float(stock[38]) if stock[38] != '' else None,
                'PE': float(stock[39]) if stock[39] != '' else None,
                'unknown': stock[40],
                'high_2': float(stock[41]),  # 意义不明
                'low_2': float(stock[42]),  # 意义不明
                '振幅': float(stock[43]),  # 换成英文
                '流通市值': float(stock[44]) if stock[44] != '' else None,  # 换成英文
                '总市值': float(stock[45]) if stock[44] != '' else None,  # 换成英文
                'PB': float(stock[46]),
                '涨停价': float(stock[47]),  # 换成英文
                '跌停价': float(stock[48])  # 换成英文
            }
        return stock_dict
