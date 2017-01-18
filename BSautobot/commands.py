from .globals import *
from . import builder


def cmdParser(text):
    print(buildings)
    params = text.split()

    if params[0] == '!ап':
        if params[1]: builder.doUpgrade(params[1])
        else: builder.doUpgrade