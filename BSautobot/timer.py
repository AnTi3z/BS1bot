import time
import threading
import logging

from . import globalobjs
from . import builder
from . import tools
from . import war

upgrTimerThread = None
feedTimerThread = None
resTimerThread = None
pplTimerThread = None

logger = logging.getLogger(__name__)

def setUpgrTimer(minutes, bld, repeat=None):
    global upgrTimerThread
    global upgrTimerStoptime
    global upgrTimerBuilding
    global upgrTimerRepeat

    if upgrTimerThread: upgrTimerThread.cancel()
    upgrTimerThread = threading.Timer(minutes*60, builder.doUpgrade, args=[bld,repeat])
    upgrTimerThread.daemon = True
    upgrTimerThread.start()
    upgrTimerStoptime = time.time() + minutes*60
    upgrTimerBuilding = bld
    upgrTimerRepeat = repeat
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
    #Запускаем таймер только если до апгрейда останется больше 2 минут... иначе апргрейд сам запустит новый таймер
    if upgrTimerStoptime - time.time() + minutes*60 > 2:
        #if resTimerThread: resTimerThread.cancel()
        resTimerThread = threading.Timer(minutes*60, tools.doTargetReses, args=[gold,wood,stone,food])
        resTimerThread.daemon = True
        resTimerThread.start()
        resTimerStoptime = time.time() + minutes*60
        globalobjs.SendInfo_cb('\U0001f553 Таймер сохранения золота установлен на %d\U0001f553 минут.' % minutes)

def setPplTimer(minutes):
    global pplTimerThread
    global pplTimerStoptime

    if pplTimerThread: pplTimerThread.cancel()
    retire = not war.imune and not war.battle #Забираем с производства людей, если нет имуна и не идет бой
    logger.debug('Забираем людей с производства? - %s', str(retire))
    pplTimerThread = threading.Timer(minutes*60, tools.doAutoPpl, args=[retire])
    pplTimerThread.daemon = True
    pplTimerThread.start()
    pplTimerStoptime = time.time() + minutes*60
    globalobjs.SendInfo_cb('\U0001f553 Таймер на отправку людей установлен на %d\U0001f553 минут.' % minutes)
    pass
