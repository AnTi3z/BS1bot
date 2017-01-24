from .globalobjs import *
from . import builder


def cmdParser(text):
    params = text.split()

    if params[0] == '!ап':
        if len(params) > 1: builder.doUpgrade(params[1])
        else: builder.doUpgrade()