from .sina import Sina
from .leverfun import Leverfun


def use(source):
    if source in ['sina']:
        return Sina()
    if source in ['leverfun', 'lf']:
        return Leverfun()
