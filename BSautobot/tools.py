import time
import logging

from . import globalobjs
from .globalobjs import *
from . import queues
from . import builder
from . import timer
from . import war

logger = logging.getLogger(__name__)

def doBuyReses(wood=0, stone=0, food=0):
    if wood == 0 and stone == 0 and food == 0: return

    queues.queThrdsLock.acquire()
    #Закупаем ресурсы
    queues.msgQueAdd('Наверх')
    queues.msgQueAdd('Торговля')
    queues.msgQueAdd('Купить')

    if wood > 0:
        queues.msgQueAdd('Дерево')
        queues.msgQueAdd(str(wood))
        queues.msgQueAdd('Назад')

    if stone > 0:
        queues.msgQueAdd('Камень')
        queues.msgQueAdd(str(stone))
        queues.msgQueAdd('Назад')

    if food > 0:
        queues.msgQueAdd('Еда')
        queues.msgQueAdd(str(food))
        queues.msgQueAdd('Назад')

    #queues.msgQueAdd('Наверх')
    queues.queThrdsLock.release()

    globalobjs.SendInfo_cb('\u26a0 Закупка: %d\U0001f332 %d\u26cf %d\U0001f356' % (wood,stone,food))

def doBuyFood():
    #Если идет бой, откладываем таймер на 1 минуту
    if war.battle:
        timer.setFeedTimer(1)
        return
    
    if resources['time'] < int(time.time()/60):
        queues.queThrdsLock.acquire()
        queues.msgQueAdd('Наверх')
        queues.queThrdsLock.release()
        #Запустить таймер на 5 секунд или time.sleep(5)
        queues.cmdQueAdd(('feed',))
        return

    hrsReserv = FOOD_RESERV_TIME

    foodConsum = (buildings['Дома']['lvl'] - min(buildings['Склад']['lvl'],buildings['Ферма']['lvl'])) * 10
    foodReserv = foodConsum * hrsReserv * 60
    storCapacity = (buildings['Склад']['lvl']*50 + 1000) * buildings['Склад']['lvl']
    foodReserv = min(storCapacity, foodReserv)
    foodNeed = foodReserv - resources['food']
    #Необходимое количество еды
    if foodNeed < 0: foodNeed = 0
    #Если золота не хватает - покупаем еду на все деньги
    elif foodNeed > resources['gold'] / 2:
        foodNeed = int(resources['gold']/2)
        foodReserv = foodNeed + resources['food']

    #Покупка
    doBuyReses(food=foodNeed)

    #Корректировка времени на которое расчитан запас еды
    if foodConsum * hrsReserv * 60 > foodReserv: hrsReserv = foodReserv / (foodConsum * 60)

    #Следующая покупка через половину времени на которое у нас запас
    if AUTOFEED: timer.setFeedTimer(int(hrsReserv*60/2))

def doTargetReses(gold=0, wood=0, stone=0, food=0):
    #Если идет бой, откладываем таймер на 1 минуту
    if war.battle:
        timer.setResTimer(1,gold,wood,stone,food)
        return
    
    if resources['time'] < int(time.time()/60):
        queues.queThrdsLock.acquire()
        queues.msgQueAdd('Наверх')
        queues.queThrdsLock.release()
        #Запустить таймер на 5 секунд или time.sleep(5)
        queues.cmdQueAdd(('reses',gold, wood, stone, food))
        return
    
    food = 0 #пока без учета еды

    woodToBuy = 0
    stoneToBuy = 0
    maxWood = wood
    maxStone = stone

    #Закупаемся до MIN_GOLD но не реже чем раз в SAVE_MONEY_TIME

    if (resources['gold'] > MIN_GOLD):
        #Оставшееся время до накопления необходимого количества золота
        if gold > resources['gold']: timetoGold = int((gold - resources['gold'])/builder.getIncom('Ратуша'))
        else: timetoGold = 0
        #Оставшееся время до накопления необходимого количества дерева
        if wood > resources['wood']: timetoWood = int((wood - resources['wood'])/min(buildings['Лесопилка']['lvl'],buildings['Склад']['lvl']))
        else: timetoWood = 0
        #Оставшееся время до накопления необходимого количества камня
        if stone > resources['stone']: timetoStone = int((stone - resources['stone'])/min(buildings['Шахта']['lvl'],buildings['Склад']['lvl']))
        else: timetoStone = 0

        logger.debug('timetoGold: %d; timetoWood: %d; timetoStone: %d',timetoGold, timetoWood, timetoStone)

        #Закупаемся максимум до MIN_GOLD
        moneyToSpend = resources['gold'] - MIN_GOLD
        moneyToSpend = max(moneyToSpend,0)

        logger.debug('Money to spend: %d',moneyToSpend)

        if timetoGold < timetoWood and timetoGold < timetoStone:
            #Закупаем ресурсы пропорционально оставшемуся времени
            woodToBuy = int((moneyToSpend/2) * (timetoWood/(timetoWood+timetoStone)))
            stoneToBuy = int((moneyToSpend/2) * (timetoStone/(timetoWood+timetoStone)))
        elif timetoGold < timetoWood:
            #Закупаем только дерево
            woodToBuy = int((moneyToSpend/2))
        elif timetoGold < timetoStone:
            #Закупаем только камень
            stoneToBuy = int((moneyToSpend/2))
        else: return

        logger.debug('woodToBuy: %d; stoneToBuy: %d',woodToBuy,stoneToBuy)

        #Проверяем что закупаем не слишком много
        if gold > MIN_GOLD:
            lastPeriod = int((gold - MIN_GOLD)/builder.getIncom('Ратуша'))
            logger.debug('Расчетное время последней закупки: %d минут',lastPeriod)
            maxWood = wood - lastPeriod * min(buildings['Лесопилка']['lvl'],buildings['Склад']['lvl'])
            maxWood = max(maxWood,0)
            maxStone = stone - lastPeriod * min(buildings['Шахта']['lvl'],buildings['Склад']['lvl'])
            maxStone = max(maxStone,0)

        if woodToBuy > 0 and resources['wood'] + woodToBuy > maxWood: woodToBuy = maxWood - resources['wood']
        woodToBuy = max(woodToBuy,0)
        if stoneToBuy > 0 and resources['stone'] + stoneToBuy > maxStone: stoneToBuy = maxStone - resources['stone']
        stoneToBuy = max(stoneToBuy,0)
            
        logger.debug('maxWood: %d; woodToBuy: %d; maxStone: %d; stoneToBuy: %d',maxWood,woodToBuy,maxStone,stoneToBuy)

        #Закупаем
        if woodToBuy > 0 or stoneToBuy >0:
            globalobjs.SendInfo_cb('\U0001f4ac Сохраняем золото.')
            doBuyReses(wood=woodToBuy, stone=stoneToBuy)

    #Вероятно потребуются еще закупки
    if (resources['wood'] + woodToBuy) < maxWood or (resources['stone'] + stoneToBuy) < maxStone:
        expectTime = int((MAX_GOLD - (resources['gold'] - woodToBuy*2 - stoneToBuy*2))/builder.getIncom('Ратуша')) + 1
        if expectTime < 1: expectTime = 1
        if expectTime > SAVE_MONEY_TIME: expectTime = SAVE_MONEY_TIME
        timer.setResTimer(expectTime,gold,wood,stone,food)

def doAutoPpl(retire=True):
    #Обновить информацию о людях если требуется
    if buildings['time'] < int(time.time()/60):
        queues.queThrdsLock.acquire()
        queues.msgQueAdd('Наверх')
        queues.msgQueAdd('Постройки')
        queues.queThrdsLock.release()
        #Запустить таймер на 5 секунд или time.sleep(5)
        queues.cmdQueAdd(('ppl',retire))
        return

    #Если доход с человека больше 2, то оставляем в домах не меньше чем макс.население минус прирост в минуту
    pplHome = buildings['Дома']['ppl']
    logger.debug('В домах всего: %d людей', pplHome)
    if builder.getIncom('Ратуша')/builder.getMaxPpl('Дома') > 2:
        pplHome -= builder.getMaxPpl('Дома') - buildings['Дома']['lvl']
        pplHome = max(0,pplHome)
        #Сколько останется в домах
    pplHomeReserv = buildings['Дома']['ppl'] - pplHome
    logger.debug('Забираем максимум: %d людей', pplHome)
    #Сначала заполняем Стену, Требушет и Казармы
    for bldRecep in ('Стена','Требушет','Казармы'):
        pplNeed = builder.getMaxPpl(bldRecep) - buildings[bldRecep]['ppl']
        logger.debug('Войска: %s - %d/%d', bldRecep, buildings[bldRecep]['ppl'],builder.getMaxPpl(bldRecep))
        if pplNeed > 0:
            #globalobjs.SendInfo_cb('\U0001f4ac Пополняем войска в %s.' % bldRecep)
            #Свободными людьми
            pplSend = min(pplNeed,pplHome)
            builder.doSendPpl(bldRecep,pplSend)
            pplNeed -= pplSend
            pplHome -= pplSend
            #Если мы не в бою и не под имуном - восстанавливаем оборону за счет производств и оставшихся в домах людей
            logger.debug('Имун: %s; Война: %s',str(war.imune),str(war.battle))
            if not war.imune and not war.battle:
                logger.debug('Полностью восстанавливаем оборону за счет производств')
                #Если не хватает людей снимаем из: Лесопилка,Шахта,Ферма,Склад
                for bldDonor in ('Лесопилка','Шахта','Ферма','Склад'):
                    if pplNeed > 0 and buildings[bldDonor]['ppl'] > 0:
                        pplSend = min(pplNeed,buildings[bldDonor]['ppl'])
                        #Если в резерве много людей, то сначла отправляем из резерва - а потом снимаем с производства
                        if pplHomeReserv > pplSend:
                            builder.doSendPpl(bldRecep,pplSend)
                            builder.doRetPpl(bldDonor,pplSend)
                        else:
                            builder.doRetPpl(bldDonor,pplSend)
                            builder.doSendPpl(bldRecep,pplSend)
                        pplNeed -= pplSend
                        buildings[bldDonor]['ppl'] -= pplSend
                    else: break
                #Если не хватило людей с производств - отправляем из домов
                if pplNeed > 0 and pplHomeReserv > 0:
                    logger.debug('Полностью восстанавливаем оборону из резерва %d людей из домов',pplHomeReserv)
                    pplSend = min(pplNeed,pplHomeReserv)
                    builder.doSendPpl(bldRecep,pplSend)
                    pplNeed -= pplSend
                    pplHomeReserv -= pplSend

    #Отправляем людей на производства (Резерв в домах не трогаем)
    if pplHome > 0:
        #globalobjs.SendInfo_cb('\U0001f4ac Отправляем людей на производство.')
        for bld in ('Склад','Ферма','Шахта','Лесопилка'):
            pplNeed = builder.getMaxPpl(bld) - buildings[bld]['ppl']
            if pplNeed > 0:
                pplSend = min(pplNeed,pplHome)
                builder.doSendPpl(bld,pplSend)
                pplNeed -= pplSend
                pplHome -= pplSend
                if pplHome <= 0: break


    if pplHome <= 0:
        timer.setPplTimer(2)
        #Если свободных людей 0 - запускаем таймер на 1 минуту
