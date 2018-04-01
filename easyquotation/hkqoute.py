# coding:utf8

import re

from .basequotation import BaseQuotation

"""
url = "http://sqt.gtimg.cn/utf8/q=r_hk00981"

url 参数改动
股票代码 q=r_hk00981
"""


class HKQuote(BaseQuotation):
    """腾讯免费行情获取"""
    stock_api = "http://sqt.gtimg.cn/utf8/q="

    def _gen_stock_prefix(self, stock_codes):
        return ['r_hk{}'.format(code) for code in stock_codes]

    def format_response_data(self, rep_data, prefix=False):
        stocks_detail = ''.join(rep_data)

        stock_dict = {}
        for raw_quotation in re.findall('v_r_hk\d+=".*?"', stocks_detail):
            quotation = re.search('"(.*?)"', raw_quotation).group(1).split('~')
            stock_dict[quotation[2]] = dict(
                lotSize=float(quotation[0]),
                name=quotation[1],
                price=float(quotation[3]),
                lastPrice=float(quotation[4]),
                openPrice=float(quotation[5]),
                amount=float(quotation[6]),
                time=quotation[30],
                high=float(quotation[33]),
                low=float(quotation[34]),
            )
        return stock_dict
