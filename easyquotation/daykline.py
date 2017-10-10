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
url = "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq&param=hk00001,day,,,660,qfq&r=0.7773272375526847"

url 参数改动
股票代码 :hk00001
日k线天数：660

更改为需要获取的股票代码和天数例如：

url = "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq&param=hk00700,day,,,350,qfq&r=0.7773272375526847"

"""


class DayKline(BaseQuotation):
    """腾讯免费行情获取"""
    stock_api = "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq&param=%s,day,,,%s,qfq&r=0.7773272375526847"
    max_num = 1

    def format_response_data(self, rep_data, prefix=False):
        stocks_detail = ''.join(rep_data)
        stock_detail_split = stocks_detail.split('kline_dayqfq=')
        # print(stock_details)
        stock_dict = dict()
        for daykline in stock_detail_split:
            # stock_detail_split = stocks_detail.split('kline_dayqfq=')
            # if len(stock_detail_split) == 2:
            #     _,daykline = stock_detail_split
            try:
                daykline = json.loads(daykline)
            except Exception as e:
                print(e)
                continue
            # print(daykline)
            daykline= daykline.get("data")
            # print(daykline)
            for key, value in daykline.items():
                stock_code = key
                _stmt = value['qfqday']
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
        if len(params) > 1:
            stock_code = params[0]
            days = params[1]
        else:
            stock_code = params
            days = 360
        url = yarl.URL(self.stock_api %(stock_code,days), encoded=True)
        print(url)
        try:
            async with self._session.get(url, timeout=10, headers=headers) as r:
                asyncio.sleep(0.1)
                response_text = await r.text()
                # print(response_text)
                return  response_text
        except asyncio.TimeoutError:
            return ''

    def get_stock_data(self, stock_list,days=360, **kwargs):
        coroutines = []

        for params in stock_list:
            coroutine = self.get_stocks_by_range(params,days)
            coroutines.append(coroutine)
            # time.sleep(0.02)
            # break
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        res = loop.run_until_complete(asyncio.gather(*coroutines))
        print()
        return self.format_response_data([x for x in res if x is not None], **kwargs)


if __name__ == "__main__":
    pass
    