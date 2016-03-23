from datetime import datetime

from .basequotation import BaseQuotation


class Tencent(BaseQuotation):
    """腾讯免费行情获取"""
    stock_api = 'http://qt.gtimg.cn/q='
    max_num = 60

    def format_response_data(self, rep_data):
        stocks_detail = ''.join(rep_data)
        stock_details = stocks_detail.split(';')
        stock_dict = dict()
        for stock_detail in stock_details:
            stock = stock_detail.split('~')
            if len(stock) <= 49:
                continue
            stock_dict[stock[2]] = {
                'name': stock[1],
                'code': stock[2],
                'now': float(stock[3]),
                'close': float(stock[4]),
                'open': float(stock[5]),
                'volume': float(stock[6]) * 100,
                'bid_volume': int(stock[7]) * 100,
                'ask_volume': float(stock[8]) * 100,
                'bid1': float(stock[9]),
                'bid1_volume': int(stock[10]) * 100,
                'bid2': float(stock[11]),
                'bid2_volume': int(stock[12]) * 100,
                'bid3': float(stock[13]),
                'bid3_volume': int(stock[14]) * 100,
                'bid4': float(stock[15]),
                'bid4_volume': int(stock[16]) * 100,
                'bid5': float(stock[17]),
                'bid5_volume': int(stock[18]) * 100,
                'ask1': float(stock[19]),
                'ask1_volume': int(stock[20]) * 100,
                'ask2': float(stock[21]),
                'ask2_volume': int(stock[22]) * 100,
                'ask3': float(stock[23]),
                'ask3_volume': int(stock[24]) * 100,
                'ask4': float(stock[25]),
                'ask4_volume': int(stock[26]) * 100,
                'ask5': float(stock[27]),
                'ask5_volume': int(stock[28]) * 100,
                '最近逐笔成交': stock[29],  # 换成英文
                'datetime': datetime.strptime(stock[30], '%Y%m%d%H%M%S'),
                '涨跌': float(stock[31]),  # 换成英文
                '涨跌(%)': float(stock[32]),  # 换成英文
                'high': float(stock[33]),
                'low': float(stock[34]),
                '价格/成交量(手)/成交额': stock[35],  # 换成英文
                '成交量(手)': int(stock[36]) * 100,  # 换成英文
                '成交额(万)': float(stock[37]) * 10000,  # 换成英文
                'turnover': float(stock[38]) if stock[38] != '' else None,
                'PE': float(stock[39]) if stock[39] != '' else None,
                'unknown': stock[40],
                'high_2': float(stock[41]),  # 意义不明
                'low_2': float(stock[42]),  # 意义不明
                '振幅': float(stock[43]),  # 换成英文
                '流通市值': float(stock[44]) if stock[44] != '' else None,  # 换成英文
                '总市值': float(stock[45]) if stock[44] != '' else None,  # 换成英文
                'PB': float(stock[46]),
                '涨停价': float(stock[47]),  # 换成英文
                '跌停价': float(stock[48])  # 换成英文
            }
        return stock_dict
