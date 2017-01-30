from . import globalobjs
import time
import threading
from . import builder
from . import feeder

upgrTimerThread = None
feedTimerThread = None

def setUpgrTimer(bld, minutes):
    global upgrTimerThread
    global upgrTimerStoptime

    if upgrTimerThread: upgrTimerThread.cancel()
    upgrTimerThread = threading.Timer(minutes*60, builder.doUpgrade, args=[bld])
    upgrTimerThread.daemon = True
    upgrTimerThread.start()
    upgrTimerStoptime = time.time() + minutes*60
    globalobjs.SendInfo_cb('\U0001f4ac Таймер на апгрейд %s установлен на %d\U0001f553 минут.' % (bld,minutes))

def setFeedTimer(minutes):
    global feedTimerThread
    global feedTimerStoptime

    if feedTimerThread: feedTimerThread.cancel()
    feedTimerThread = threading.Timer(minutes*60, feeder.doBuyFood)
    feedTimerThread.daemon = True
    feedTimerThread.start()
    feedTimerStoptime = time.time() + minutes*60
    globalobjs.SendInfo_cb('\U0001f4ac Таймер на закупку еды\U0001f356 установлен на %d\U0001f553 минут.' % minutes)