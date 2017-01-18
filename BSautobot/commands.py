from .globals import *


def cmdParser(text):
    params = text.split()
    if params[0] == '!ап': buildings.doUpgrade(params[1])