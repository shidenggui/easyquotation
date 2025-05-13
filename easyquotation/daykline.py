# coding:utf8
"""
# pylint: disable=line-too-long
url = "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq&param=hk00001,day,,,660,qfq&r=0.7773272375526847"

url 参数改动
股票代码 :hk00001
日k线天数：660

更改为需要获取的股票代码和天数例如：

# pylint: disable=line-too-long
url = "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq&param=hk00700,day,,,350,qfq&r=0.7773272375526847"

"""
import json
import re

from . import basequotation
from . import helpers


class DayKlineBase(basequotation.BaseQuotation):
    max_num = 1

    def _gen_stock_prefix(self, stock_codes, day=1500):
        stock_codes = [code if code.startswith('hk') else helpers.get_stock_type(code) + code[-6:] for code in stock_codes ]
        return ["{},day,,,{},qfq".format(code, day) for code in stock_codes]

    def format_response_data(self, rep_data, **kwargs):
        stock_dict = {}
        for raw_quotation in rep_data:
            stock_details = json.loads(raw_quotation)
            if not stock_details["data"]:
                continue
            for stock_code, value in stock_details["data"].items():
                if "qfqday" in value:
                    stock_detail = value["qfqday"]
                else:
                    stock_detail = value.get("day")
                if stock_detail is None:
                    print("stock code data not find %s"%stock_code)
                    continue
                stock_dict[stock_code] = {'klines': stock_detail}
                if self.withqt and 'qt' in value:
                    stock_qt = helpers.tencent_quote(value['qt'][stock_code])
                    stock_dict[stock_code]['qt'] = stock_qt
                break

        return stock_dict

    def get_klines(self, stock_codes, day=1500, withqt=True):
        """返回指定股票的K线数据
        :param stock_codes: 股票代码或股票代码列表，
                示例：'sh000001' / ['sz000001', 'sz000002']
        :param day: 要获取的天数
        :param withqt: 这个接口会返回基本行情数据，不需要可以设置为False
        :return: k线行情字典，键为股票代码，值为k线数据和实时行情。
        """
        self.withqt = withqt
        stock_list = self._gen_stock_prefix(stock_codes, day)
        res = self._fetch_stock_data(stock_list)
        return self.format_response_data(res)


class HKDayKline(DayKlineBase):
    """腾讯免费行情获取"""

    max_num = 1
    @property
    def stock_api(self) -> str:
        # pylint: disable=line-too-long
        return "http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=&param="

    def _gen_stock_prefix(self, stock_codes, day=1500):
        stock_codes = [c if c.startswith('hk') else 'hk'+c for c in stock_codes]
        return ["{},day,,,{},qfq".format(code, day) for code in stock_codes]


class CNDayKline(DayKlineBase):
    """腾讯免费行情获取"""

    max_num = 1

    @property
    def stock_api(self) -> str:
        # pylint: disable=line-too-long
        return "http://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=&param="

    def _gen_stock_list(self, stock_codes, day=1500):
        return ["{},day,,,{},qfq".format(code, day) for code in stock_codes]


class DayKline():
    """腾讯免费行情获取"""

    def get_klines(self, stock_codes, day=1500, withqt=True):
        """返回指定股票的K线数据 可以是港股或者A股
        :param stock_codes: 股票代码或股票代码列表，不带前缀默认A股
                示例：'000001' / 'sh000001' / ['000001', '000002']
        :param day: 要获取的天数
        :return: 行情字典，键为股票代码，值为实时行情。
        """
        if not isinstance(stock_codes, list):
            stock_codes = [stock_codes]

        hkcodes = [c for c in stock_codes if c.startswith('hk')]
        hkklines = {}
        if hkcodes:
            hkklines = HKDayKline().get_klines(hkcodes, day, withqt)

        cncodes = [c for c in stock_codes if c not in hkcodes]
        cnklines = {}
        if cncodes:
            cnklines = CNDayKline().get_klines(cncodes, day, withqt)

        return {**cnklines, **hkklines}


if __name__ == "__main__":
    pass
