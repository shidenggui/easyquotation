import re
import json
import asyncio
import aiohttp
from . import helpers


class Sina:
    """新浪免费行情获取"""

    def __init__(self):
        self.grep_stock_detail = re.compile(r'(\d+)=([^\s][^,]+?)%s%s' % (r',([\.\d]+)' * 29, r',([-\.\d:]+)' * 2))
        self.sina_stock_api = 'http://hq.sinajs.cn/?format=text&list='
        self.stock_data = []
        self.stock_codes = []
        self.stock_with_exchange_list = []
        self.max_num = 800
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
        async with aiohttp.get(self.sina_stock_api + self.stock_list[index]) as r:
            response_text = await r.text()
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
        result = self.grep_stock_detail.finditer(stocks_detail)
        stock_dict = dict()
        for stock_match_object in result:
            stock = stock_match_object.groups()
            stock_dict[stock[0]] = dict(
                name=stock[1],
                open=float(stock[2]),
                close=float(stock[3]),
                now=float(stock[4]),
                high=float(stock[5]),
                low=float(stock[6]),
                buy=float(stock[7]),
                sell=float(stock[8]),
                turnover=int(stock[9]),
                volume=float(stock[10]),
                bid1_volume=int(stock[11]),
                bid1=float(stock[12]),
                bid2_volume=int(stock[13]),
                bid2=float(stock[14]),
                bid3_volume=int(stock[15]),
                bid3=float(stock[16]),
                bid4_volume=int(stock[17]),
                bid4=float(stock[18]),
                bid5_volume=int(stock[19]),
                bid5=float(stock[20]),
                ask1_volume=int(stock[21]),
                ask1=float(stock[22]),
                ask2_volume=int(stock[23]),
                ask2=float(stock[24]),
                ask3_volume=int(stock[25]),
                ask3=float(stock[26]),
                ask4_volume=int(stock[27]),
                ask4=float(stock[28]),
                ask5_volume=int(stock[29]),
                ask5=float(stock[30]),
                date=stock[31],
                time=stock[32],
            )
        return stock_dict
