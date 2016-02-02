from .sina import Sina
from .leverfun import Leverfun
from .jsl import Jsl


def use(source):
    if source in ['sina']:
        return Sina()
    if source in ['leverfun', 'lf']:
        return Leverfun()
    if source in ['jsl']:
        return Jsl()
