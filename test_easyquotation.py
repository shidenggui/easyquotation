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


if __name__ == '__main__':
    unittest.main()
