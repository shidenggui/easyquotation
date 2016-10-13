import asyncio
import json

import aiohttp
import easyutils

from . import helpers


class BaseQuotation:
    """行情获取基类"""
    max_num = 800  # 每次请求的最大股票数
    stock_api = ''  # 股票 api

    def __init__(self):
        self._session = None
        stock_codes = self.load_stock_codes()
        self.stock_list = self.gen_stock_list(stock_codes)

    def gen_stock_list(self, stock_codes):
        stock_with_exchange_list = [easyutils.stock.get_stock_type(code) + code[-6:] for code in stock_codes]

        stock_list = []
        request_num = len(stock_codes) // self.max_num + 1
        for range_start in range(request_num):
            num_start = self.max_num * range_start
            num_end = self.max_num * (range_start + 1)
            request_list = ','.join(stock_with_exchange_list[num_start:num_end])
            stock_list.append(request_list)
        return stock_list

    @staticmethod
    def load_stock_codes():
        with open(helpers.stock_code_path()) as f:
            return json.load(f)['stock']

    @property
    def all(self):
        return self.get_stock_data(self.stock_list)

    def stocks(self, stock_codes):
        if type(stock_codes) is not list:
            stock_codes = [stock_codes]

        stock_list = self.gen_stock_list(stock_codes)
        return self.get_stock_data(stock_list)

    async def get_stocks_by_range(self, params):
        headers = {
            'Accept-Encoding': 'gzip'
        }
        async with self._session.get(self.stock_api + params, timeout=5, headers=headers) as r:
            response_text = await r.text()
            return response_text

    def get_stock_data(self, stock_list):
        self._session = aiohttp.ClientSession()
        coroutines = []

        for params in stock_list:
            coroutine = self.get_stocks_by_range(params)
            coroutines.append(coroutine)
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        res = loop.run_until_complete(asyncio.gather(*coroutines))

        self._session.close()
        return self.format_response_data(res)

    def format_response_data(self, rep_data):
        pass
