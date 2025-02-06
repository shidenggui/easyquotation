# coding:utf8
"""
url = "http://sqt.gtimg.cn/utf8/q=r_hk00981"

url 参数改动
股票代码 q=r_hk00981
"""


import re

from . import basequotation


class HKQuote(basequotation.BaseQuotation):
    """腾讯免费行情获取"""

    @property
    def stock_api(self) -> str:
        return "http://sqt.gtimg.cn/utf8/q="

    def _gen_stock_prefix(self, stock_codes):
        return ["r_hk{}".format(code) for code in stock_codes]

    def format_response_data(self, rep_data, **kwargs):
        stocks_detail = "".join(rep_data)

        stock_dict = {}
        for raw_quotation in re.findall(r'v_r_hk\d+=".*?"', stocks_detail):
            quotation = re.search('"(.*?)"', raw_quotation).group(1).split("~")
            stock_dict[quotation[2]] = dict(
                lotSize=float(quotation[0]),                  #              每手数量
                name=quotation[1],                            #              股票名称
                price=float(quotation[3]),                    # now price,   股票当前价格
                lastPrice=float(quotation[4]),                # pre_close,   股票昨天收盘价格
                openPrice=float(quotation[5]),                #              股票今天开盘价格
                amount=float(quotation[6]),                   # volume,      股票成交量 
                now_1=float(quotation[9]),                    #              当前价格1
                now_2=float(quotation[19]),                   #              当前价格2
                volume_2=float(quotation[29]),                #              成交量2
                date=(quotation[30][:10]).replace("/", "-"),  #              当前日期
                time=quotation[30][-8:],                      #              当前时间
                Pchange=float(quotation[31]),                 #              涨跌   , Price change
                dtd=float(quotation[32]),                     # PCR,         涨跌(%), Price Change Ratio 
                high=float(quotation[33]),                    #              当天最高价格
                low=float(quotation[34]),                     #              当天最低价格
                now_3=float(quotation[35]),                   #              当前价格3
                volume_3=float(quotation[36]),                #              成交量3
                amountYuan=float(quotation[37]),              # true amount, 成交额
                Amp=float(quotation[43]),                     #              振幅
                FFMCap=float(quotation[44]),                  #              流通市值, Free Float MarketCap
                MarketCap=float(quotation[45]),               #              总市值, Market Capacity               
                year_high=float(quotation[48]),               #              52周最高价 
                year_low=float(quotation[49]),                #              52周最低价  
                ODR=float(quotation[51]),                     #              委比, Order Difference Ratio --> (委买-委卖)*100/(委买+委卖) 
                turnover=float(quotation[59]),                #              换手率(%) 
                lotSize_2=float(quotation[60]),               #              lotSize_2 
                FF=float(quotation[69]),                      #              流通股本, Free Float
                TE=float(quotation[70]),                      #              总股本, Total Equity
                MA=float(quotation[73]),                      #              均价, Moving Average                 
            )
        return stock_dict
