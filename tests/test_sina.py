# coding:utf-8

import unittest

import easyquotation


class TestSina(unittest.TestCase):
    MOCK_DATA = 'var hq_str_sz162411="华宝油气,0.489,0.488,0.491,0.492,0.488,0.490,0.491,133819867,65623147.285,2422992,0.490,4814611,0.489,2663142,0.488,1071900,0.487,357900,0.486,5386166,0.491,8094689,0.492,6087538,0.493,2132373,0.494,5180900,0.495,2019-03-12,15:00:03,00";\n'

    def setUp(self):
        self._sina = easyquotation.use("sina")

    def test_extract_stock_name(self):
        """
        fix https://github.com/shidenggui/easyquotation/issues/51
        """
        stock_name = self._sina.format_response_data(self.MOCK_DATA)["162411"][
            "name"
        ]
        self.assertEqual(stock_name, "华宝油气")
