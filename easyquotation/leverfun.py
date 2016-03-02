import asyncio

import aiohttp


class Leverfun:
    stock_api = 'https://app.leverfun.com/timelyInfo/timelyOrderForm'

    def __init__(self):
        self.stocks_dict = dict()

    def stocks(self, stock_codes):
        if type(stock_codes) is not list:
            stock_codes = [stock_codes]

        threads = []
        for stock in stock_codes:
            threads.append(self.get_stock_detail(stock))

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.wait(threads))
        return self.stocks_dict

    async def get_stock_detail(self, stock_code):
        params = dict(stockCode=stock_code)
        async with aiohttp.get(Leverfun.stock_api, params=params) as r:
            r_json = await r.json()
            self.stocks_dict[stock_code] = Leverfun.format_response_data(r_json)

    @classmethod
    def format_response_data(cls, response_data):
        data = response_data['data']
        buys = data['buyPankou']
        sells = data['sellPankou']
        stock_dict = dict(
                close=round(data['preClose'], 3),
                now=data['match'],
                buy=buys[0]['price'],
                sell=sells[0]['price'],
        )
        for trade_info_li, name in zip([sells, buys], ['ask', 'bid']):
            for i, trade_info in enumerate(trade_info_li):
                stock_dict['{name}{index}'.format(name=name, index=i + 1)] = trade_info['price']
                stock_dict['{name}{index}_volume'.format(name=name, index=i + 1)] = trade_info['volume'] * 100
        return stock_dict


if __name__ == '__main__':
    q = Leverfun()
    print(q.stocks(['000001', '162411']))
    print(q.stocks('162411'))
