import re
import json
import asyncio
import requests
from . import helper

class Sina:
    """新浪免费行情获取"""

    def __init__(self):
        self.grep_stock_detail = re.compile(r'(\d+)="([^,]+?)%s' % (r',([\.\d]+)' * 29, ))
        self.sina_stock_api = 'http://hq.sinajs.cn/list='
        self.stock_data = []
        self.stock_codes = []
        self.stock_with_exchange_list = []
        self.max_num = 800
        self.load_stock_codes()

    def load_stock_codes(self):
        with open(helper.stock_code_path()) as f:
            self.stock_codes = json.load(f)['stock']

    @property
    def all(self):
        return self.get_stock_data()

    async def get_stocks_by_range(self, start):
        num_start = self.max_num * start
        num_end = self.max_num * (start + 1)
        stock_list = ','.join(self.stock_with_exchange_list[num_start:num_end])

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, requests.get, self.sina_stock_api + stock_list)

        self.stock_data.append(response.text)

    def get_stock_data(self):
        if not self.stock_with_exchange_list:
            self.stock_with_exchange_list = list(
                map(lambda stock_code: ('sh%s' if stock_code.startswith(('5', '6', '9')) else 'sz%s') % stock_code,
                    self.stock_codes))

        threads = []
        for x in range(len(self.stock_with_exchange_list) // self.max_num):
            threads.append(self.get_stocks_by_range(x))
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(threads))

        return self.format_response_data()

    def format_response_data(self):
        result = self.grep_stock_detail.findall(''.join(self.stock_data))
        stock_dict = dict()
        for stock in result:
            stock_dict[stock[0]] = dict(
                name=stock[1],
                open=stock[2],
                close=stock[3],
                now=stock[4],
                high=stock[5],
                low=stock[6],
                buy=stock[7],
                sell=stock[8],
                turnover=stock[9],
                volume=stock[10],
                bid1_volume=stock[11],
                bid1=stock[12],
                bid2_volume=stock[13],
                bid2=stock[14],
                bid3_volume=stock[15],
                bid3=stock[16],
                bid4_volume=stock[17],
                bid4=stock[18],
                bid5_volume=stock[19],
                bid5=stock[20],
                ask1_volume=stock[21],
                ask1=stock[22],
                ask2_volume=stock[23],
                ask2=stock[24],
                ask3_volume=stock[25],
                ask3=stock[26],
                ask4_volume=stock[27],
                ask4=stock[28],
                ask5_volume=stock[29],
                ask5=stock[30],
            )
        return stock_dict

if __name__ == '__main__':
    import pprint; pprint.pprint(Sina().all['162411'])
