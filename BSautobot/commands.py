import time
from .globalobjs import *
from . import builder
from . import feeder
from . import timer
from . import globalobjs

def cmdParser(text):
    params = text.split()

    if params[0] == '!ап':
        if len(params) > 1: builder.doUpgrade(params[1])
        else:
            if timer.upgrTimerThread and timer.upgrTimerThread.isAlive():
                globalobjs.SendInfo_cb('\U0001f4ac Таймер на апгрейд здания уже запущен. Осталось %d\U0001f553 минут.' % int((timer.upgrTimerStoptime - time.time())/60))
            else: builder.doUpgrade()
    elif params[0] == '!еда':
        if timer.feedTimerThread and timer.feedTimerThread.isAlive():
            globalobjs.SendInfo_cb('\U0001f4ac Таймер на закупку еды уже запущен. Осталось %d\U0001f553 минут.' % int((timer.feedTimerStoptime - time.time())/60))
        else: feeder.doBuyFood()
