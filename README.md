# easyquotation

[![Package](https://img.shields.io/pypi/v/easyquotation.svg)](https://pypi.python.org/pypi/easyquotation)
[![License](https://img.shields.io/github/license/shidenggui/easyquotation.svg)](https://github.com/shidenggui/easyquotation/blob/master/LICENSE)


快速获取新浪/腾讯的全市场行情, 网络正常的情况下只需要 `200+ms`

### 前言
* 获取新浪的免费实时行情
* 获取腾讯财经的免费实时行情
* 获取集思路的数据

### 微信群以及公众号

欢迎大家扫码关注公众号「食灯鬼」，一起交流。进群可通过菜单加我好友，备注量化。

![公众号二维码](https://gitee.com/shidenggui/assets/raw/master/uPic/mp-qr.png)

若二维码因 Github 网络无法打开，请点击[公众号二维码](https://gitee.com/shidenggui/assets/raw/master/uPic/mp-qr.png)直接打开图片。

### Author

**easyquotation** © [shidenggui](https://github.com/shidenggui), Released under the [MIT](./LICENSE) License.<br>

> Blog [@shidenggui](https://shidenggui.com) · Weibo [@食灯鬼](https://www.weibo.com/u/1651274491) · Twitter [@shidenggui](https://twitter.com/shidenggui)
>


### 其他作品

* [easytrader 股票程序化交易库](https://github.com/shidenggui/easytrader)
* [easyquant 简单的量化框架](https://github.com/shidenggui/easyqutant)

### requirements

> Python 3.6+
 
### 安装

```python
pip install easyquotation
```

也可以下载源码，然后安装

```python
python setup.py install
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
# prefix 指定返回行情的股票代码是否带 sz/sh/bj 市场前缀
quotation.market_snapshot(prefix=True) 
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

```python
quotation.real('162411') # 支持直接指定前缀，如 'sh000001'
```

##### 多只股票

```python
quotation.real(['000001', '162411']) 
```

##### 同时获取指数和行情
```python
# 获取相同代码的指数和股票时 prefix 必须为 True
quotation.real(['sh000001', 'sz000001'], prefix=True)
```

#### 更新内置全市场股票代码

```python
easyquotation.update_stock_codes()
```


##### 港股日k线图
*[腾讯日k线图](http://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?_var=kline_dayqfq&param=hk00700,day,,,350,qfq&r=0.7773272375526847)*

```python

import easyquotation
quotation  = easyquotation.use("daykline")
data = quotation.real(['00001','00700'])
print(data)

```python
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

##### 腾讯港股实时行情 
*[腾讯控股实时行情](http://sqt.gtimg.cn/utf8/q=r_hk00700)*
```python

import easyquotation
quotation = easyquotation.use("hkquote")
data = quotation.real(['00001','00700'])
print(data)
```

```python
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

#### 选择 [jsl](https://www.jisilu.cn)（集思录） 行情

```python
quotation = easyquotation.use('jsl') 
```

##### 设置 cookie (可选)

不设置的话获取相关数据有限制

```python
quotation.set_cookie('从浏览器获取的集思录 Cookie')
```


##### 指数ETF查询接口

**TIP :** 尚未包含黄金ETF和货币ETF

*[集思录ETF源网页](https://www.jisilu.cn/data/etf/#tlink_2)*

```python
quotation.etfindex(index_id="", min_volume=0, max_discount=None, min_discount=None)
```

**return**

```python
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

