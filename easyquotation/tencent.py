# coding:utf8
import re
from typing import Optional

from . import basequotation
from . import helpers

class Tencent(basequotation.BaseQuotation):
    """腾讯免费行情获取"""

    grep_stock_code = re.compile(r"(?<=_)\w+")
    max_num = 60

    @property
    def stock_api(self) -> str:
        return "http://qt.gtimg.cn/q="

    def format_response_data(self, rep_data, prefix=False):
        stocks_detail = "".join(rep_data)
        stock_details = stocks_detail.split(";")
        stock_dict = dict()
        for stock_detail in stock_details:
            stock = stock_detail.split("~")
            if len(stock) <= 49:
                continue
            stock_code = (
                self.grep_stock_code.search(stock[0]).group()
                if prefix
                else stock[2]
            )
            stock_dict[stock_code] = helpers.tencent_quote(stock)
        return stock_dict

    def _safe_acquire_float(self, stock: list, idx: int) -> Optional[float]:
        """
        There are some securities that only have 50 fields. See example below:
        ['\nv_sh518801="1',
        '国泰申赎',
        '518801',
        '2.229',
        ......
         '', '0.000', '2.452', '2.006', '"']
        """
        try:
            return self._safe_float(stock[idx])
        except IndexError:
            return None

    def _safe_float(self, s: str) -> Optional[float]:
        try:
            return float(s)
        except ValueError:
            return None
