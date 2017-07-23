# coding:utf8
import re
import time

import aiohttp
import asyncio
import easyutils
import yarl
from .basequotation import BaseQuotation

#url = "http://data.gtimg.cn/flashdata/hushen/minute/sz000001.js?maxage=110&0.28163905744440854"
#url = "http://data.gtimg.cn/flashdata/hushen/minute/%s.js?maxage=110&0.28163905744440854"



class TimeKline(BaseQuotation):
    """腾讯免费行情获取"""
    stock_api = 'http://data.gtimg.cn/flashdata/hushen/minute/'
    max_num = 1

    def format_response_data(self, rep_data, prefix=False):
        stocks_detail = ''.join(rep_data)
        stock_details = stocks_detail.split(';')
        stock_dict = dict()
        for stock_detail in stock_details:
            # print(stock_detail)
            # print(stock_detail.split('~'))
            stock_detail_split = stock_detail.split('~')
            if len(stock_detail_split) == 2:
                stock_code,ktime_line = stock_detail_split
            else:
                for row in stock_detail_split:
                    break
            ktime_data = ktime_line.split('\n')
            # print(ktime_data)
            ktime_date = ktime_data[1].split(":")[1][:-3]
            ktime_line_data = ktime_data[2:]
            time_data_dict = {}
            for row in ktime_data[2:]:
                point_data = row.split(" ")
                if len(point_data) < 3:
                    continue
                else:
                    k_time = point_data[0]
                    k_price = point_data[1]
                    k_volume = point_data[2][:-3]
                    print_data_dict = {
                        "20" + ktime_date + k_time: [k_time,k_price,k_volume]
                    }
                    time_data_dict.update(print_data_dict)
            stock_dict[stock_code] = {
                "date" : ktime_date,
                "time_data": time_data_dict
            }

        return stock_dict

    async def get_stocks_by_range(self, params):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        headers = {
            'Accept-Encoding': 'gzip, deflate, sdch',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36'
        }
        url = yarl.URL(self.stock_api + params +".js", encoded=True)
        print(url)
        try:
            async with self._session.get(url, timeout=10, headers=headers) as r:
                asyncio.sleep(0.1)
                response_text = await r.text()
                # print(response_text)
                return params + "~"+ response_text
        except asyncio.TimeoutError:
            return None

    def get_stock_data(self, stock_list, **kwargs):
        coroutines = []

        for params in stock_list:
            coroutine = self.get_stocks_by_range(params)
            coroutines.append(coroutine)
            # time.sleep(0.02)
            # break
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        res = loop.run_until_complete(asyncio.gather(*coroutines))

        return self.format_response_data([x for x in res if x is not None], **kwargs)

    def gen_stock_list(self, stock_codes):
        stock_with_exchange_list = [easyutils.stock.get_stock_type(code) + code[-6:] for code in stock_codes]

        if len(stock_with_exchange_list) < self.max_num:
            request_list = ','.join(stock_with_exchange_list)
            return [request_list]

        stock_list = []
        request_num = len(stock_codes) // self.max_num + 1
        for range_start in range(request_num):
            num_start = self.max_num * range_start
            num_end = self.max_num * (range_start + 1)
            request_list = ','.join(stock_with_exchange_list[num_start:num_end])
            stock_list.append(request_list)
        return stock_list



if __name__ == "__main__":
    data = TimeKline()
    print(data)
