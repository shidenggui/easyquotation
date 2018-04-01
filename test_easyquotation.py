# coding:utf8
import unittest

import easyquotation


class TestEasyquotation(unittest.TestCase):
    def test_stock_code_with_prefix(self):
        cases = ['sina', 'qq']
        for src in cases:
            q = easyquotation.use(src)
            data = q.all_market
            for k in data.keys():
                self.assertRegex(k, r'(sh|sz)\d{6}')

    def test_all(self):
        cases = ['sina', 'qq']
        for src in cases:
            q = easyquotation.use(src)
            data = q.all
            for k in data.keys():
                self.assertRegex(k, r'\d{6}')


class TestHqouteQuotatin(unittest.TestCase):
    MOCK_RESPONSE_DATA = 'v_r_hk00700="100~腾讯控股~00700~409.600~412.200~414.000~41115421.0~0~0~409.600~0~0~0~0~0~0~0~0~0~409.600~0~0~0~0~0~0~0~0~0~41115421.0~2018/03/29 16:08:11~-2.600~-0.63~417.000~405.200~409.600~41115421.0~16899465578.300~0~44.97~~0~0~2.86~38909.443~38909.443~TENCENT~0.21~476.600~222.400~0.40~0~0~0~0~0~0~42.25~12.70~"; v_r_hk00980="100~联华超市~00980~2.390~2.380~2.380~825000.0~0~0~2.390~0~0~0~0~0~0~0~0~0~2.390~0~0~0~0~0~0~0~0~0~825000.0~2018/03/29 16:08:11~0.010~0.42~2.440~2.330~2.390~825000.0~1949820.000~0~-5.38~~0~0~4.62~8.905~26.758~LIANHUA~0.00~4.530~2.330~1.94~0~0~0~0~0~0~-0.01~0.94~";'

    def setUp(self):
        self._obj = easyquotation.use('hkquote')

    def test_format_response_data(self):
        excepted = {'00700': {'amount': 41115421.0,
                              'high': 417.0,
                              'lastPrice': 412.2,
                              'lotSize': 100.0,
                              'low': 405.2,
                              'name': '腾讯控股',
                              'openPrice': 414.0,
                              'price': 409.6,
                              'time': '2018/03/29 16:08:11'},
                    '00980': {'amount': 825000.0,
                              'high': 2.44,
                              'lastPrice': 2.38,
                              'lotSize': 100.0,
                              'low': 2.33,
                              'name': '联华超市',
                              'openPrice': 2.38,
                              'price': 2.39,
                              'time': '2018/03/29 16:08:11'}}
        result = self._obj.format_response_data(self.MOCK_RESPONSE_DATA)
        self.assertDictEqual(result, excepted)


if __name__ == '__main__':
    unittest.main()
