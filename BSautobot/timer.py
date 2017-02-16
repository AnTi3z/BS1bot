import time
import threading

from . import globalobjs
from . import builder
from . import tools

upgrTimerThread = None
feedTimerThread = None
resTimerThread = None

def setUpgrTimer(minutes, bld):
    global upgrTimerThread
    global upgrTimerStoptime

    if upgrTimerThread: upgrTimerThread.cancel()
    upgrTimerThread = threading.Timer(minutes*60, builder.doUpgrade, args=[bld])
    upgrTimerThread.daemon = True
    upgrTimerThread.start()
    upgrTimerStoptime = time.time() + minutes*60
    globalobjs.SendInfo_cb('\U0001f553 Таймер на апгрейд %s установлен на %d\U0001f553 минут.' % (bld,minutes))

def setFeedTimer(minutes):
    global feedTimerThread
    global feedTimerStoptime

    if feedTimerThread: feedTimerThread.cancel()
    feedTimerThread = threading.Timer(minutes*60, tools.doBuyFood)
    feedTimerThread.daemon = True
    feedTimerThread.start()
    feedTimerStoptime = time.time() + minutes*60
    globalobjs.SendInfo_cb('\U0001f553 Таймер на закупку еды\U0001f356 установлен на %d\U0001f553 минут.' % minutes)

def setResTimer(minutes, gold, wood, stone, food):
    global resTimerThread
    global resTimerStoptime

    if resTimerThread: resTimerThread.cancel()
    #Запускаем таймер только если до/после апгрейда останется больше 2 минут... иначе апргрейд сам запустит новый таймер
    if abs(upgrTimerStoptime - time.time() + minutes*60) > 2:
        #if resTimerThread: resTimerThread.cancel()
        resTimerThread = threading.Timer(minutes*60, tools.doTargetReses, args=[gold,wood,stone,food])
        resTimerThread.daemon = True
        resTimerThread.start()
        resTimerStoptime = time.time() + minutes*60
        globalobjs.SendInfo_cb('\U0001f553 Таймер сохранения золота установлен на %d\U0001f553 минут.' % minutes)
