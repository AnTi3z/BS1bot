import time

from . import globalobjs
from .globalobjs import *
from . import builder
from . import tools
from . import timer

def cmdParser(text):
    cmd, *params = text.split()

    if cmd == '!ап':
        if len(params) > 0:
            if params[0] == 'стоп':
                if timer.upgrTimerThread: timer.upgrTimerThread.cancel()
                globalobjs.SendInfo_cb('\U0001f4ac Таймер на апгрейд остановлен.')
            else: builder.doUpgrade(*params)
        else:
            if timer.upgrTimerThread and timer.upgrTimerThread.isAlive():
                if timer.upgrTimerRepeat: txtRepeat = "(еще %d раз)" % timer.upgrTimerRepeat
                else: txtRepeat = ""
                globalobjs.SendInfo_cb('\U0001f4ac Таймер на апгрейд %s%s уже запущен. Осталось %d\U0001f553 минут.' % (timer.upgrTimerBuilding,txtRepeat,int((timer.upgrTimerStoptime - time.time())/60)))
            else: builder.doUpgrade()
    elif cmd == '!еда':
        if len(params) > 0:
            if params[0] == 'стоп':
                if timer.feedTimerThread: timer.feedTimerThread.cancel()
                globalobjs.SendInfo_cb('\U0001f4ac Таймер на закупку еды остановлен.')
        else:
            if timer.feedTimerThread and timer.feedTimerThread.isAlive():
                globalobjs.SendInfo_cb('\U0001f4ac Таймер на закупку еды уже запущен. Осталось %d\U0001f553 минут.' % int((timer.feedTimerStoptime - time.time())/60))
            else: tools.doBuyFood()
