# coding:utf8

from .boc import Boc
from .jsl import Jsl
from .sina import Sina
from .tencent import Tencent


def use(source):
    if source in ['sina']:
        return Sina()
    if source in ['jsl']:
        return Jsl()
    if source in ['qq', 'tencent']:
        return Tencent()
    if source in ['boc']:
        return Boc()
    if source in ["timekline"]:
        from .timekline import TimeKline
        return TimeKline()
    if source in ['daykline']:
        from .daykline import DayKline
        return DayKline()
    if source in ['hkquote']:
        from .hkqoute import HKQuote
        return HKQuote()
