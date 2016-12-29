# coding:utf8
import sys

from .boc import Boc
from .jsl import Jsl
from .leverfun import Leverfun
from .sina import Sina
from .tencent import Tencent

PY_VERSION = sys.version_info[:2]
if PY_VERSION < (3, 5):
    raise Exception('Python 版本需要 3.5 或以上, 当前版本为 %s.%s 请升级 Python' % PY_VERSION)


def use(source):
    if source in ['sina']:
        return Sina()
    if source in ['leverfun', 'lf']:
        return Leverfun()
    if source in ['jsl']:
        return Jsl()
    if source in ['qq', 'tencent']:
        return Tencent()
    if source in ['boc']:
        return Boc()
