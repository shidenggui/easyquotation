# coding:utf8
import unittest
from unittest import mock

import easyquotation


class TestTimeklineQuotation(unittest.TestCase):
    MOCK_RESPONSE_DATA = [
        (
            "000001",
            'min_data="\\n\\\ndate:180413\\n\\\n0930 11.64 29727\\n\\\n0931 11.65 52410\\n\\\n";',
        )
    ]

    def setUp(self):
        self._obj = easyquotation.use("timekline")

    @mock.patch(
        "easyquotation.timekline.basequotation.BaseQuotation._fetch_stock_data"
    )
    def test_fetch_stock_data(self, mock_super_fetch):
        test_cases = [
            (["000001"], ["test_data"], [("000001", "test_data")]),
            (
                ["000001", "000002"],
                ["test_data", None],
                [("000001", "test_data")],
            ),
            ([], [], []),
        ]
        for stock_list, resp_data, expected in test_cases:
            mock_super_fetch.return_value = resp_data
            res = self._obj._fetch_stock_data(stock_list)
            self.assertListEqual(res, expected)

    def test_format_response_data(self):
        excepted = {
            "000001": {
                "date": "20180413",
                "time_data": [
                    ["0930", "11.64", "29727"],
                    ["0931", "11.65", "52410"],
                ],
            }
        }

        result = self._obj.format_response_data(self.MOCK_RESPONSE_DATA)
        self.assertDictEqual(result, excepted)


if __name__ == "__main__":
    unittest.main()
