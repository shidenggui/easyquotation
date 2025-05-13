# coding:utf8

from . import boc, daykline, hkquote, jsl, sina, tencent
from . import minuteskline

# pylint: disable=too-many-return-statements
def use(source):
    if source in ["sina"]:
        return sina.Sina()
    if source in ["jsl"]:
        return jsl.Jsl()
    if source in ["qq", "tencent"]:
        return tencent.Tencent()
    if source in ["boc"]:
        return boc.Boc()
    if source in ['kline', "daykline"]:
        return daykline.DayKline()
    if source in ['mkline', 'minkline']:
        return minuteskline.MinutesKline()
    if source in ["hkquote"]:
        return hkquote.HKQuote()
    raise NotImplementedError
