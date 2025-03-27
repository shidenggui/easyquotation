# coding:utf8
import abc
import json
import multiprocessing.pool
import warnings

import requests

from . import helpers


class BaseQuotation(metaclass=abc.ABCMeta):
    """行情获取基类"""

    max_num = 800  # 每次请求的最大股票数

    @property
    @abc.abstractmethod
    def stock_api(self) -> str:
        """
        行情 api 地址
        """
        pass

    def __init__(self):
        self._session = requests.session()
        stock_codes = self.load_stock_codes()
        self.stock_list = self.gen_stock_list(stock_codes)

    def gen_stock_list(self, stock_codes):
        stock_with_exchange_list = self._gen_stock_prefix(stock_codes)

        if self.max_num > len(stock_with_exchange_list):
            request_list = ",".join(stock_with_exchange_list)
            return [request_list]

        stock_list = []
        for i in range(0, len(stock_codes), self.max_num):
            request_list = ",".join(
                stock_with_exchange_list[i : i + self.max_num]
            )
            stock_list.append(request_list)
        return stock_list

    def _gen_stock_prefix(self, stock_codes):
        return [
            helpers.get_stock_type(code) + code[-6:] for code in stock_codes
        ]

    @staticmethod
    def load_stock_codes():
        with open(helpers.STOCK_CODE_PATH) as f:
            return json.load(f)["stock"]

    @property
    def all(self):
        warnings.warn("use market_snapshot instead", DeprecationWarning)
        return self.get_stock_data(self.stock_list)

    @property
    def all_market(self):
        """return quotation with stock_code prefix key"""
        return self.get_stock_data(self.stock_list, prefix=True)

    def stocks(self, stock_codes, prefix=False):
        """deprecated, use real instead"""
        warnings.warn("use real instead", DeprecationWarning)
        return self.real(stock_codes, prefix)

    def real(self, stock_codes, prefix=False):
        """返回指定股票的实时行情
        :param stock_codes: 股票代码或股票代码列表，
                示例：'000001' / 'sh000001' / ['000001', '000002'] 
        :param prefix: 如果prefix为True，返回的行情字典键以sh/sz/bj市场标识开头
                    如果prefix为False，返回的行情将无法区分指数和股票代码，例如 sh000001 上证指数和 sz000001 平安银行
        :return: 行情字典，键为股票代码，值为实时行情。
        """
        if not isinstance(stock_codes, list):
            stock_codes = [stock_codes]

        stock_list = self.gen_stock_list(stock_codes)
        return self.get_stock_data(stock_list, prefix=prefix)

    def market_snapshot(self, prefix=False):
        """return all market quotation snapshot
        :param prefix: if prefix is True, return quotation dict's  stock_code
             key start with sh/sz market flag
        """
        return self.get_stock_data(self.stock_list, prefix=prefix)

    def get_stocks_by_range(self, params):
        headers = self._get_headers()
        r = self._session.get(self.stock_api + params, headers=headers)
        return r.text

    def _get_headers(self) -> dict:
        return {
            "Accept-Encoding": "gzip, deflate, sdch",
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/54.0.2840.100 "
                "Safari/537.36"
            ),
        }

    def get_stock_data(self, stock_list, **kwargs):
        """获取并格式化股票信息"""
        res = self._fetch_stock_data(stock_list)
        return self.format_response_data(res, **kwargs)

    def _fetch_stock_data(self, stock_list):
        """获取股票信息"""
        pool = multiprocessing.pool.ThreadPool(len(stock_list))
        try:
            res = pool.map(self.get_stocks_by_range, stock_list)
        finally:
            pool.close()
        return [d for d in res if d is not None]

    def format_response_data(self, rep_data, **kwargs):
        pass
