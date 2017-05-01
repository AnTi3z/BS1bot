import time
import logging
import threading

from . import globalobjs
from .globalobjs import *
from . import builder
from . import tools
from . import timer
from . import queues
from . import war

logger = logging.getLogger(__name__)

def cmdParser(text):
    cmd, *params = text.split()

    if cmd == '!ап':
        if len(params) > 0:
            if params[0] == 'стоп':
                if timer.upgrTimerThread: timer.upgrTimerThread.cancel()
                globalobjs.SendInfo_cb('\U0001f4ac Таймер на апгрейд остановлен.')
            else:
                threading.Thread(target=builder.doUpgrade,args=params).start()
        else:
            if timer.upgrTimerThread and timer.upgrTimerThread.isAlive():
                if timer.upgrTimerRepeat: txtRepeat = "(еще %d раз)" % timer.upgrTimerRepeat
                else: txtRepeat = ""
                globalobjs.SendInfo_cb('\U0001f4ac Таймер на апгрейд %s%s уже запущен. Осталось %d\U0001f553 минут.' % (timer.upgrTimerBuilding,txtRepeat,int((timer.upgrTimerStoptime - time.time())/60)))
            else:
                threading.Thread(target=builder.doUpgrade).start()
    elif cmd == '!еда':
        if len(params) > 0:
            if params[0] == 'стоп':
                if timer.feedTimerThread: timer.feedTimerThread.cancel()
                globalobjs.SendInfo_cb('\U0001f4ac Таймер на закупку еды остановлен.')
        else:
            if timer.feedTimerThread and timer.feedTimerThread.isAlive():
                globalobjs.SendInfo_cb('\U0001f4ac Таймер на закупку еды уже запущен. Осталось %d\U0001f553 минут.' % int((timer.feedTimerStoptime - time.time())/60))
            else:
                threading.Thread(target=tools.doBuyFood).start()
    elif cmd == '!люди':
        threading.Thread(target=tools.doAutoPpl).start()
    elif cmd == '!поиск':
        if len(params) > 0:
            if params[0] == 'стоп': war.searching = False
            else:
                war.searching = True
                threading.Thread(target=war.findTarget,kwargs={'name': params[0]}).start()
