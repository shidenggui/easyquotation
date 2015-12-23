from .sina import Sina


def use(source):
    if source in ['sina']:
        return Sina()
