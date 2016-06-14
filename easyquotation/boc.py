import re
import requests

from .basequotation import BaseQuotation


class Boc(object):
    """中行美元最新汇率"""
    url = 'http://www.boc.cn/sourcedb/whpj/'

    def get_exchange_rate(self, currency='usa'):
        rep = requests.get(self.url)
        data = re.findall(r'<td>(.*?)</td>', rep.text)

        if currency == 'usa':
            return {
                'sell': data[-13],
                'buy': data[-15]
            }