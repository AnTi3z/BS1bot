import threading

from . import globalobjs
from .globalobjs import *
from . import builder
from . import timer
from . import queues

cooldown = None
imune = None
battle = False
defense = False
target = {}
searching = False

def endBattle():
    battle = False
    target = {}
    #Обновить информацию об имеющейся голде и обновить время имуна и кд через меню войны
    with queues.queThrdsLock:
        queues.msgQueAdd('Наверх')
        queues.msgQueAdd('Война')
        queues.queStoped.wait()
        #Если требуется - починить стену
        if buildings['Стена']['str'] < 100*buildings['Стена']['lvl']:
            queues.msgQueAdd('Наверх')
            queues.msgQueAdd('Постройки')
            queues.msgQueAdd('Стена')
            queues.msgQueAdd('Чинить')

    #Перезапустить апгрейд
    if timer.upgrTimerThread:
        timer.upgrTimerThread.cancel()
        threading.Thread(target=builder.doUpgrade,args=(timer.upgrTimerBuilding, timer.upgrTimerRepeat)).start()
    logger.debug('war.battle=%s; war.imune=%s; war.cooldown=%s',str(battle),str(imune),str(cooldown))

def findTarget(name=None, karma=2, land=10000, srch_all=False):
    if srch_all: srch_cmd = 'Всех'
    else: srch_cmd = 'Подходящих'
    with queues.queThrdsLock:
        queues.msgQueAdd('Наверх')
        queues.msgQueAdd('Война')
        queues.msgQueAdd(srch_cmd)
        queues.queStoped.wait()
        if name:
            while searching and target['name'] != name:
                queues.msgQueAdd(srch_cmd)
                queues.queStoped.wait()
        else:
            while searching and target['karma'] < karma and target['land'] < land:
                queues.msgQueAdd(srch_cmd)
                queues.queStoped.wait()
        globalobjs.SendInfo_cb('\u26a0 Поиск цели завершен. Цель: %s' % target['name'])
        logger.debug('Searching complete! Target=%s',str(target))
                
