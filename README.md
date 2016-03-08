# easyquotation

### 前言
* 获取新浪的免费实时行情
* 获取腾讯财经的免费实时行情
* 获取 `leverfun` 的免费 `Level 2` 十档行情
* 获取集思路的分级基金数据
* 有兴趣的可以加群 `429011814` 一起讨论

**开发环境** : `Ubuntu 15.10` / `Python 3.5`

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

#### 选择 sina 行情

```python
quotation = easyquotation.use('sina')
```

#### 获取所有股票行情

```python
quotation.all
```

**return**

```python
 {'000159': {'name': '国际实业', # 股票名
  'buy': '8.87', # 竞买价
  'sell': '8.88', # 竞卖价
  'now': '8.88', # 现价
  'open': '8.99', # 开盘价
  'close': '8.96', # 昨日收盘价
  'high': '9.15', # 今日最高价
  'low': '8.83', # 今日最低价
  'turnover': '22545048', # 交易股数
  'volume': '202704887.74'， # 交易金额
  'ask1': '8.88', # 卖一价
  'ask1_volume': '111900', # 卖一量
  'ask2': '8.89',
  'ask2_volume': '54700',
  'bid1': '8.87', # 买一价
  'bid1_volume': '21800', # 买一量
  ...
  'bid2': '8.86', 
  'bid2_volume': '78400',
  'date': '2016-02-19',
  'time': '14:30:00',
  ...},
  ......
}
```

#### 选择 tencent 行情

```python
quotation = easyquotation.use('tencent') # or qq
```

#### 获取所有股票行情

```python
quotation.all
```

#### 选择 leverfun 免费十档行情

```
quotation = easyquotation.use('lf') # ['leverfun', 'lf']
```

#### 获取十档行情

##### 单只股票

```
quotation.stocks('162411')
```

##### 多只股票

```
quotation.stocks(['000001', '162411'])
```

**return**

```python
 {'000159': {'buy': '8.87', # 竞买价
  'sell': '8.88', # 竞卖价
  'now': '8.88', # 现价
  'close': '8.96', # 昨日收盘价
  'ask1': '8.88', # 卖一价
  'ask1_volume': '111900', # 卖一量
  'ask2': '8.89',
  'ask2_volume': '54700',
  'bid1': '8.87', # 买一价
  'bid1_volume': '21800', # 买一量
  ...
  'bid2': '8.86', 
  'bid2_volume': '78400',
  ...},
  ......
}
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

*****return**

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
quotation.fundarb(jsl_username, jsl_password, avolume=100, bvolume=100, ptype='price'):

```
参数意义
jsl_username: 集思录用户名
jsl_password: 集思路登录密码
avolume: A成交额，单位百万
bvolume: B成交额，单位百万
ptype: 溢价计算方式，price=现价，buy=买一，sell=卖一
```

** return ** 

对应的分级 A 数据
        """以字典形式返回分级A数据

#### 更新股票代码

```
easyquotation.update_stock_codes()
```
