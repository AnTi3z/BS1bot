import time
from .globalobjs import *
from . import builder
from . import timer
from . import globalobjs

def cmdParser(text):
    params = text.split()

    if params[0] == '!ап':
        if timer.upgrTimerThread and timer.upgrTimerThread.isAlive():
            globalobjs.SendInfo_cb('\U0001f4ac Таймер на апгрейд здания уже запущен. Осталось %d минут.' % int((timer.upgrTimerStoptime - time.time())/60))
        else:
            if len(params) > 1: builder.doUpgrade(params[1])
            else: builder.doUpgrade()
