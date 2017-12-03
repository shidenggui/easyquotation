# coding:utf8
import re
import time
import json

import aiohttp
import asyncio
import easyutils
import yarl
from .basequotation import BaseQuotation

"""
url = "http://sqt.gtimg.cn/utf8/q=r_hk00981"

url 参数改动
股票代码 q=r_hk00981
"""


class HKQuote(BaseQuotation):
    """腾讯免费行情获取"""
    stock_api = "http://sqt.gtimg.cn/utf8/q=r_hk%s"
    max_num = 1

    def format_response_data(self, rep_data, prefix=False):
        stocks_detail = ''.join(rep_data)
        stock_detail_split = stocks_detail.split('v_r_hk')
        stock_dict = dict()
        for data in stock_detail_split:
            _stmt = {}
            try:
                stock_code,stock_data= data.split("=")
                _stmt["stock_code"] = stock_code
            except Exception as e:
                print(e)
                continue
            try:
                stock_data_split = stock_data.split("~")
                row = stock_data_split
                _stmt_data = dict(
                lotSize = row[0],
                name = row[1],
                price = row[3],
                lastPrice = row[4],
                openPrice= row[5],
                amount = row[6],
                time = row[30],
                high = row[33],
                low = row[34],
                )
                _stmt.update(_stmt_data)
            except expression as identifier:
                continue
      

            stock_dict[stock_code] = _stmt

        return stock_dict

    async def get_stocks_by_range(self, *params):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
        }
        print(params)
        stock_code = params[0]
        url = yarl.URL(self.stock_api %(stock_code), encoded=True)
        print(url)
        try:
            async with self._session.get(url, timeout=10, headers=headers) as r:
                asyncio.sleep(0.1)
                response_text = await r.text()
                # print(response_text)
                return  response_text
        except asyncio.TimeoutError:
            return ''

    def get_stock_data(self, stock_list, **kwargs):
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
        return self.format_response_data([x for x in res if x is not None], **kwargs)

    def stock_data():
        try:
            import ConfigParser as config

        except Exception as e:
            import configparser as config
        data = config.ConfigParser("./hk_stock_codes.conf")
        stock_codes = data.get("stock_code")


if __name__ == "__main__":
    pass
