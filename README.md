# easyquotation

### 前言
* 用于获取新浪的免费实时行情
* 有兴趣的可以加群 `429011814` 一起讨论

**开发环境** : `Ubuntu 15.10` / `Python 3.5`

### requirements

> Python 3.5+
 
> pip install -r requirements.txt

### 用法

#### 引入:

```python
import easyquotation
```

#### 选择 sina 行情

```python
quotation = essyquotation.use('sina')
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
  'ask3': '8.90',
  'ask3_volume': '12000',
  'ask4': '8.91',
  'ask4_volume': '4400',
  'ask5': '8.92',
  'ask5_volume': '47313',
  'bid1': '8.87', # 买一价
  'bid1_volume': '21800', # 买一量
  'bid2': '8.86', 
  'bid2_volume': '78400',
  'bid3': '8.85',
  'bid3_volume': '51598',
  'bid4': '8.84',
  'bid4_volume': '25500',
  'bid5': '8.83',
  'bid5_volume': '39600'},
  ......
}
```
