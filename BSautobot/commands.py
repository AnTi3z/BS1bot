import time
import logging
import threading

from . import globalobjs
from .globalobjs import *
from . import builder
from . import tools
from . import timer
from . import queues

logger = logging.getLogger(__name__)

def cmdParser(text):
    cmd, *params = text.split()

    if cmd == '!ап':
        if len(params) > 0:
            if params[0] == 'стоп':
                if timer.upgrTimerThread: timer.upgrTimerThread.cancel()
                globalobjs.SendInfo_cb('\U0001f4ac Таймер на апгрейд остановлен.')
            else:
                builder.doUpgrade(*params)
        else:
            if timer.upgrTimerThread and timer.upgrTimerThread.isAlive():
                if timer.upgrTimerRepeat: txtRepeat = "(еще %d раз)" % timer.upgrTimerRepeat
                else: txtRepeat = ""
                globalobjs.SendInfo_cb('\U0001f4ac Таймер на апгрейд %s%s уже запущен. Осталось %d\U0001f553 минут.' % (timer.upgrTimerBuilding,txtRepeat,int((timer.upgrTimerStoptime - time.time())/60)))
            else:
                upgrader = threading.Thread(target=builder.doUpgrade,name='upgr')
                upgrader.start()
    elif cmd == '!еда':
        if len(params) > 0:
            if params[0] == 'стоп':
                if timer.feedTimerThread: timer.feedTimerThread.cancel()
                globalobjs.SendInfo_cb('\U0001f4ac Таймер на закупку еды остановлен.')
        else:
            if timer.feedTimerThread and timer.feedTimerThread.isAlive():
                globalobjs.SendInfo_cb('\U0001f4ac Таймер на закупку еды уже запущен. Осталось %d\U0001f553 минут.' % int((timer.feedTimerStoptime - time.time())/60))
            else:
                feeder = threading.Thread(target=tools.doBuyFood,name='feed')
                feeder.start()
    elif cmd == '!люди':
        people = threading.Thread(target=tools.doAutoPpl,name='ppl')
        people.start()
    elif cmd == '!тест':
        t = threading.Thread(target=test)
        t.start()

def test():
    logger.debug("Создали тестовый поток")
    queues.queThrdsLock.acquire()
    queues.msgQueAdd('Наверх')
    queues.msgQueAdd('Инфо')
    queues.msgQueAdd('Постройки')
    queues.msgQueAdd('Стена')
    #while not queues.que_stoped:
    #    logger.debug('queue wait...')
    #    time.sleep(1)
    queues.wait()
    logger.debug("Прочность стены 1: %d", buildings['Стена']['str'])
    queues.msgQueAdd('Чинить')
    queues.wait()
    logger.debug("Прочность стены 2: %d", buildings['Стена']['str'])
    queues.msgQueAdd('Наверх')
    queues.msgQueAdd('Инфо')
    queues.wait()
    queues.queThrdsLock.release()

