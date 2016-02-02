# coding:utf8
# 获取集思路的分级数据
import json
import time

import requests


class Jsl(object):
    """
    抓取集思路的分级A数据
    """

    # 分级A的接口
    __funda_url = 'http://www.jisilu.cn/data/sfnew/funda_list/?___t={ctime:d}'

    # 分级A数据
    # 返回的字典格式
    # { 150020:
    # {'abrate': '5:5',
    #  'calc_info': None,
    #  'coupon_descr': '+3.0%',
    #  'coupon_descr_s': '+3.0%',
    #  'fund_descr': '每年第一个工作日定折，无下折，A不参与上折，净值<1元无定折',
    #  'funda_amount': 178823,
    #  'funda_amount_increase': '0',
    #  'funda_amount_increase_rt': '0.00%',
    #  'funda_base_est_dis_rt': '2.27%',
    #  'funda_base_est_dis_rt_t1': '2.27%',
    #  'funda_base_est_dis_rt_t2': '-0.34%',
    #  'funda_base_est_dis_rt_tip': '',
    #  'funda_base_fund_id': '163109',
    #  'funda_coupon': '5.75',
    #  'funda_coupon_next': '4.75',
    #  'funda_current_price': '0.783',
    #  'funda_discount_rt': '24.75%',
    #  'funda_id': '150022',
    #  'funda_increase_rt': '0.00%',
    #  'funda_index_id': '399001',
    #  'funda_index_increase_rt': '0.00%',
    #  'funda_index_name': '深证成指',
    #  'funda_left_year': '永续',
    #  'funda_lower_recalc_rt': '1.82%',
    #  'funda_name': '深成指A',
    #  'funda_nav_dt': '2015-09-14',
    #  'funda_profit_rt': '7.74%',
    #  'funda_profit_rt_next': '6.424%',
    #  'funda_value': '1.0405',
    #  'funda_volume': '0.00',
    #  'fundb_upper_recalc_rt': '244.35%',
    #  'fundb_upper_recalc_rt_info': '深成指A不参与上折',
    #  'last_time': '09:18:22',
    #  'left_recalc_year': '0.30411',
    #  'lower_recalc_profit_rt': '-',
    #  'next_recalc_dt': '<span style="font-style:italic">2016-01-04</span>',
    #  'owned': 0,
    #  'status_cd': 'N'}
    # }

    @staticmethod
    def formatjson(fundajson):
        """格式化集思录返回的json数据,以字典形式保存"""
        d = {}
        for row in fundajson['rows']:
            funda_id = row['id']
            cell = row['cell']
            d[funda_id] = cell
        return d

    def funda(self, fields=[], min_volume=0, min_discount=0, ignore_nodown=False, forever=False):
        """以字典形式返回分级A数据
        :param fields:利率范围，形如['+3.0%', '6.0%']
        :param min_volume:最小交易量，单位万元
        :param min_discount:最小折价率, 单位%
        :param ignore_nodown:是否忽略无下折品种,默认 False
        :param forever: 是否选择永续品种,默认 False
        """
        # 添加当前的ctime
        self.__funda_url = self.__funda_url.format(ctime=int(time.time()))
        # 请求数据
        rep = requests.get(self.__funda_url)
        # 获取返回的json字符串
        fundajson = json.loads(rep.text)
        # 格式化返回的json字符串
        data = self.formatjson(fundajson)
        # 过滤小于指定交易量的数据
        if min_volume:
            data = {k: data[k] for k in data if float(data[k]['funda_volume']) > min_volume}
        if len(fields):
            data = {k: data[k] for k in data if data[k]['coupon_descr_s'] in ''.join(fields)}
        if ignore_nodown:
            data = {k: data[k] for k in data if data[k]['fund_descr'].find('无下折') == -1}
        if forever:
            data = {k: data[k] for k in data if data[k]['funda_left_year'].find('永续') != -1}
        if min_discount:
            data = {k: data[k] for k in data if float(data[k]['funda_discount_rt'][:-1]) > min_discount}

        self.__funda = data
        return self.__funda
