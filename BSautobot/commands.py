import time

from .globalobjs import *
from . import builder
from . import feeder
from . import timer
from . import globalobjs

def cmdParser(text):
    cmd, *params = text.split()

    if cmd == '!ап':
        if len(params) > 0:
            if params[0] == 'стоп': pass
            else: builder.doUpgrade(params[0])
        else:
            if timer.upgrTimerThread and timer.upgrTimerThread.isAlive():
                globalobjs.SendInfo_cb('\U0001f4ac Таймер на апгрейд здания уже запущен. Осталось %d\U0001f553 минут.' % int((timer.upgrTimerStoptime - time.time())/60))
            else: builder.doUpgrade()
    elif cmd == '!еда':
        if len(params) > 0:
            if params[0] == 'стоп': pass
        else:
            if timer.feedTimerThread and timer.feedTimerThread.isAlive():
                globalobjs.SendInfo_cb('\U0001f4ac Таймер на закупку еды уже запущен. Осталось %d\U0001f553 минут.' % int((timer.feedTimerStoptime - time.time())/60))
            else: feeder.doBuyFood()
