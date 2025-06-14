# coding:utf8
"""
# pylint: disable=line-too-long

url 参数改动
股票代码 :sh603444
k线数：320

# pylint: disable=line-too-long
url = "https://ifzq.gtimg.cn/appstock/app/kline/mkline?param=sh603444,m5,,320&_var=m5_today&r=0.7732845199699612"

reference: https://stockapp.finance.qq.com/mstats/

分时数据:
https://web.ifzq.gtimg.cn/appstock/app/minute/query?_var=&code=sh603444&r=0.8169133625890732
https://web.ifzq.gtimg.cn/appstock/app/day/query?_var=&code=sh603444&r=0.8305712721067519
"""
import json

from . import basequotation
from . import helpers

class MinutesKline(basequotation.BaseQuotation):
    max_num = 1

    @property
    def stock_api(self) -> str:
        # pylint: disable=line-too-long
        return "https://ifzq.gtimg.cn/appstock/app/kline/mkline?param="

    def _gen_stock_prefix(self, stock_codes, kltype=1, minute=320):
        stock_codes = [code if code.startswith('hk') else helpers.get_stock_type(code) + code[-6:] for code in stock_codes ]
        return ["{},m{},,{}&_var=&r=0.".format(code, kltype, minute) for code in stock_codes]

    def format_response_data(self, rep_data, **kwargs):
        stock_dict = {}
        for raw_quotation in rep_data:
            stock_details = json.loads(raw_quotation)
            if not stock_details["data"]:
                continue
            for stock_code, value in stock_details["data"].items():
                stock_dict[stock_code] = {}
                for k, kv in value.items():
                    if k.startswith('m'):
                        stock_dict[stock_code]['klines'] = [[f'{x[0][0:4]}-{x[0][4:6]}-{x[0][6:8]} {x[0][8:10]}:{x[0][10:]}'] + x[1:6] for x in kv]
                    elif k == 'qt' and self.withqt:
                        stock_qt = helpers.tencent_quote(kv[stock_code])
                        stock_dict[stock_code]['qt'] = stock_qt
        return stock_dict

    def get_klines(self, stock_codes, kltype=1, minute=320, withqt=True):
        """ 返回指定股票的分钟K线数据

        Args:
            stock_codes (str or list): A single stock code or a list of stock codes to retrieve K-line data for.
            kltype (int, optional): The type of K-line to retrieve. Defaults to 1. 1, 5, 15, 30, 60
            minute (int, optional): The number of k-lines to retrieve. Defaults to 320.
            withqt (bool, optional): If True, includes additional quote data in the response. Defaults to True.

        Returns:
            dict: A dictionary containing formatted K-line data for the given stock codes.
        """

        self.withqt = withqt
        if not isinstance(stock_codes, list):
            stock_codes = [stock_codes]
        stock_list = self._gen_stock_prefix(stock_codes, kltype, minute)
        res = self._fetch_stock_data(stock_list)
        return self.format_response_data(res)

