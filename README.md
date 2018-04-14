# easyquotation

[![Package](https://img.shields.io/pypi/v/easyquotation.svg)](https://pypi.python.org/pypi/easyquotation)
[![Travis](https://img.shields.io/travis/shidenggui/easyquotation.svg)](https://travis-ci.org/shidenggui/easyquotation)
[![License](https://img.shields.io/github/license/shidenggui/easyquotation.svg)](https://github.com/shidenggui/easyquotation/blob/master/LICENSE)


快速获取新浪/腾讯的全市场行情, 网络正常的情况下只需要 `200+ms`

### 前言
* 获取新浪的免费实时行情
* 获取腾讯财经的免费实时行情
* 获取集思路的分级基金数据
* 有兴趣的可以加群 `556050652` 一起讨论
* 捐助:

![微信](http://7xqo8v.com1.z0.glb.clouddn.com/wx.png?imageView2/1/w/300/h/300)             ![支付宝](http://7xqo8v.com1.z0.glb.clouddn.com/zhifubao2.png?imageView2/1/w/300/h/300)


## 公众号

扫码关注“易量化”的微信公众号，不定时更新一些个人文章及与大家交流

![](http://7xqo8v.com1.z0.glb.clouddn.com/easy_quant_qrcode.jpg?imageView2/1/w/300/h/300)

**开发环境** : `Ubuntu 16.04` / `Python 3.5`

### requirements

> Python 3.5+
 
> pip install -r requirements.txt

### 安装

```python
pip install easyquotation
```

#### 升级

```python
pip install easyquotation --upgrade
```

### 用法

#### 引入:

```python
import easyquotation
```

#### 选择行情

```python
quotation = easyquotation.use('sina') # 新浪 ['sina'] 腾讯 ['tencent', 'qq'] 
```

#### 获取所有股票行情

```python
quotation.market_snapshot(prefix=True) # prefix 参数指定返回的行情字典中的股票代码 key 是否带 sz/sh 前缀
```

**return**

```python
 {'sh000159': {'name': '国际实业', # 股票名
  'buy': 8.87, # 竞买价
  'sell': 8.88, # 竞卖价
  'now': 8.88, # 现价
  'open': 8.99, # 开盘价
  'close': 8.96, # 昨日收盘价
  'high': 9.15, # 今日最高价
  'low': 8.83, # 今日最低价
  'turnover': 22545048, # 交易股数
  'volume': 202704887.74， # 交易金额
  'ask1': 8.88, # 卖一价
  'ask1_volume': 111900, # 卖一量
  'ask2': 8.89,
  'ask2_volume': 54700,
  'bid1': 8.87, # 买一价
  'bid1_volume': 21800, # 买一量
  ...
  'bid2': 8.86, 
  'bid2_volume': 78400,
  'date': '2016-02-19',
  'time': '14:30:00',
  ...},
  ......
}
```
 
##### 单只股票

```
quotation.real('162411') # 支持直接指定前缀，如 'sh000001'
```

##### 多只股票

```
quotation.stocks(['000001', '162411']) 
```

##### 同时获取指数和行情

```
quotation.stocks(['sh000001', 'sz000001'], prefix=True) 
```

#### 更新股票代码

```
easyquotation.update_stock_codes()
```


#### 选择 jsl 行情

```
quotation = easyquotation.use('jsl') # ['jsl']
```

##### 获取分级基金信息

```
quotation.funda() # 参数可选择利率、折价率、交易量、有无下折、是否永续来过滤

quotation.fundb() # 参数如上
```

对应的分级 A 数据

**return**

```
{ 150020:
{'abrate': '5:5',
'calc_info': None,
'coupon_descr': '+3.0%',
'coupon_descr_s': '+3.0%',
'fund_descr': '每年第一个工作日定折，无下折，A不参与上折，净值<1元无定折',
'funda_amount': 178823,
'funda_amount_increase': '0',
'funda_amount_increase_rt': '0.00%',
'funda_base_est_dis_rt': '2.27%',
'funda_base_est_dis_rt_t1': '2.27%',
'funda_base_est_dis_rt_t2': '-0.34%',
'funda_base_est_dis_rt_tip': '',
'funda_base_fund_id': '163109',
'funda_coupon': '5.75',
'funda_coupon_next': '4.75',
'funda_current_price': '0.783',
'funda_discount_rt': '24.75%',
'funda_id': '150022',
'funda_increase_rt': '0.00%',
'funda_index_id': '399001',
'funda_index_increase_rt': '0.00%',
'funda_index_name': '深证成指',
'funda_left_year': '永续',
'funda_lower_recalc_rt': '1.82%',
'funda_name': '深成指A',
'funda_nav_dt': '2015-09-14',
'funda_profit_rt': '7.74%',
'funda_profit_rt_next': '6.424%',
'funda_value': '1.0405',
'funda_volume': '0.00',
'fundb_upper_recalc_rt': '244.35%',
'fundb_upper_recalc_rt_info': '深成指A不参与上折',
'last_time': '09:18:22',
'left_recalc_year': '0.30411',
'lower_recalc_profit_rt': '-',
'next_recalc_dt': '<span style="font-style:italic">2016-01-04</span>',
'owned': 0,
'status_cd': 'N'}>'}}
```

##### 分级基金套利接口

```
quotation.fundarb(jsl_username, jsl_password, avolume=100, bvolume=100, ptype='price')
```

```
jsl_username: 集思录用户名
jsl_password: 集思路登录密码
avolume: A成交额，单位百万
bvolume: B成交额，单位百万
ptype: 溢价计算方式，price=现价，buy=买一，sell=卖一
```

**return** 
```
{
    "165511":{
        'base_fund_id': '165511',                         # 母基金代码
        'AB_price': '现价A/B : 1.008/1.329',
        'a_profit_rt_next': '4.705',
        'a_ratio': 4,
        'abrate': '4:6',
        'apply_fee': '0',
        'apply_fee_tip': '0',
        'apply_sell': '-0.59',
        'asset_ratio': '95%',
        'asset_ratio_last': '99%',
        'asset_ratio_num': '95.00',
        'b_est_val': '1.340',
        'b_gangan': '1.502',
        'b_ratio': 6,
        'base_est_dis_rt': '-0.56%',
        'base_est_val': '1.2073',
        'base_fund_nm': '信诚500',
        'base_lower_recalc_rt': '54.15%',
        'base_nav': '1.1970',
        'base_nav_dt': '2016-04-13',
        'buy1A': '1.007',
        'buy1B': '1.329',
        'buy1_amountA': '0.201',
        'buy1_amountB': '7.123',
        'buy_redeem': '-0.51',
        'calc_info': None,
        'coupon': '0.00%',
        'coupon_next': '4.700',
        'est_dis_rt': '-0.55%',
        'est_time': '2016-04-14 15:10:05',
        'fundA_amount': '6667',
        'fundA_amount_increase': '-51',
        'fundA_amount_increase_rt': '-0.76%',
        'fundA_amount_tip': '2016-04-14 A类总份额6667.000万份，份额增长-0.76%',
        'fundA_id': '150028',
        'fundA_last_dt': '2016-04-14',
        'fundA_last_time': '14:57:02',
        'fundA_nav': '1.0090',
        'fundA_nav_dt': '2016-04-13',
        'fundA_nm': '中证500A',
        'fundA_stock_volume': '28.2446',
        'fundA_stock_volume_tip': 'A类总份额6667.000万份, 成交28万份',
        'fundA_turnover_rt': '0.42%',
        'fundA_volume': '28.46',
        'fundB_amount': 10000.5,
        'fundB_amount_increase': '-76',
        'fundB_amount_tip': '2016-04-14 B类总份额10000万份，份额增长-0.76%',
        'fundB_id': '150029',
        'fundB_last_dt': '2016-04-14',
        'fundB_last_time': '15:00:27',
        'fundB_nav': '1.3220',
        'fundB_nav_dt': '2016-04-13',
        'fundB_nm': '中证500B',
        'fundB_stock_volume': '255.5280',
        'fundB_stock_volume_tip': 'B类总份额10000万份, 成交256万份',
        'fundB_turnover_rt': '2.56%',
        'fundB_volume': '337.24',
        'fund_company_nm': '信诚基金',
        'funda_name_tip': '下期利率：4.70，修正收益率：4.71%',
        'idx_incr_rt': '0.91%',
        'increase_rtA': '-0.10%',
        'increase_rtB': '1.06%',
        'index_id': '399905',
        'index_nm': '中证 500',
        'is_est_val': 1,
        'is_last_nav': 1,
        'lower_recalc_rt': '54.15',
        'maturity_dt': '-',
        'merge_price': '1.2006',
        'min_apply_amount': None,
        'notes': 'http://www.xcfunds.com/funds_2012/165511/fundinfor.shtml\r\n',
        'ownedA': 0,
        'ownedM': 1,
        'priceA': '1.008',
        'priceB': '1.329',
        'real_idx_increase_rt': '0.91',
        'recalc_to': None,
        'redeem_fee': '0.5%',
        'redeem_fee_tip': '0.5%',
        'sell1A': '1.008',
        'sell1B': '1.330',
        'sell1_amountA': '7.132',
        'sell1_amountB': '16.820',
        'status_cd': 'N'
    }
}
```

##### 指数ETF查询接口

**TIP :** 尚未包含黄金ETF和货币ETF

*[集思录ETF源网页](https://www.jisilu.cn/data/etf/#tlink_2)*

```
quotation.etfindex(index_id="", min_volume=0, max_discount=None, min_discount=None)
```

**return**

```
{
    "510050": {
        "fund_id": "510050",                # 代码
        "fund_nm": "50ETF",                 # 名称
        "price": "2.066",                   # 现价
        "increase_rt": "0.34%",             # 涨幅
        "volume": "71290.96",               # 成交额(万元)
        "index_nm": "上证50",                # 指数
        "pe": "9.038",                      # 指数PE
        "pb": "1.151",                      # 指数PB
        "index_increase_rt": "0.45%",       # 指数涨幅
        "estimate_value": "2.0733",         # 估值
        "fund_nav": "2.0730",               # 净值
        "nav_dt": "2016-03-11",             # 净值日期
        "discount_rt": "-0.34%",            # 溢价率
        "creation_unit": "90",              # 最小申赎单位(万份)
        "amount": "1315800",                # 份额
        "unit_total": "271.84",             # 规模(亿元)
        "index_id": "000016",               # 指数代码
        "last_time": "15:00:00",            # 价格最后时间(未确定)
        "last_est_time": "23:50:02",        # 估值最后时间(未确定)
    }
}
```


##### 分数图


*[腾讯分时图地址](http://data.gtimg.cn/flashdata/hushen/minute/sz000001.js)*

```python

quotation = easyquotation.use("timekline")
data = quotation.real(['603828'], prefix=True)

```

**return**

```
{
   'sh603828': {
        'date': '170721',  #日期 
        'time_data': {
            '201707210930': ['0930', '19.42', '61'], # [时间, 当前价, 上一分钟到这一分钟之间的成交数量]
            '201707210931': ['0931', '19.42','122'], 
            '201707210932': ['0932', '19.43', '123'], 
            '201707210933': ['0933', '19.48', '125'], 
            '201707210934': ['0934', '19.49', '133'], 
            '201707210935': ['0935', '19.48', '161'], 
            ...
    }
}
```

##### 港股日k线图
*[腾讯日k线图](http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq&param=hk00700,day,,,350,qfq&r=0.7773272375526847)*

```python

import easyquotation
quotation  = easyquotation.use("daykline")
data = quotation.real(['00001','00700'])
print(data)

```
*return*
```
{
    '00001': [
                ['2017-10-09', '352.00', '349.00', '353.00', '348.60', '13455864.00'], # [日期, 今开, 今收, 最高, 最低, 成交量 ]
                ['2017-10-10', '350.80', '351.20', '352.60', '349.80', '10088970.00'],
               ]
    '00700':[
        
    ]           
     }
}
```

##### 腾讯港股时时行情 
*[腾讯控股时时行情](http://sqt.gtimg.cn/utf8/q=r_hk00700)*
```python

import easyquotation
quotation = easyquotation.use("hkquote")
data = quotation.real(['00001','00700'])
print(data)
```

```
{
    '00001': 
        {
            'stock_code': '00001', # 股票代码
            'lotSize': '"100', # 每手数量
            'name': '长和', # 股票名称
            'price': '97.20', # 股票当前价格
            'lastPrice': '97.75', # 股票昨天收盘价格
            'openPrice': '97.75', # 股票今天开盘价格
            'amount': '1641463.0', # 股票成交量 
            'time': '2017/11/29 15:38:58', # 当前时间
            'high': '98.05', # 当天最高价格
            'low': '97.15' # 当天最低价格
        }, 
    '00700': 
        {
            'stock_code': '00700', 
            'lotSize': '"100',
            'name': '腾讯控股', 
            'price': '413.20', 
            'lastPrice': '419.20', 
            'openPrice': '422.20', 
            'amount': '21351010.0', 
            'time': '2017/11/29 15:39:01', 
            'high': '422.80',
            'low': '412.40'
        }
}
```
