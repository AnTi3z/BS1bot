import time

from . import globalobjs
from .globalobjs import *
from . import queues
from . import builder
from . import timer


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

    queues.msgQueAdd('Наверх')
    queues.queThrdsLock.release()

    globalobjs.SendInfo_cb('\u26a0 Закупка: %d\U0001f332 %d\u26cf %d\U0001f356' % (wood,stone,food))

def doBuyFood():
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
        if wood > resources['wood']: timetoWood = int((wood - resources['wood'])/min(buildings['Лесопилка']['ppl'],buildings['Склад']['ppl']))
        else: timetoWood = 0
        #Оставшееся время до накопления необходимого количества камня
        if stone > resources['stone']: timetoStone = int((stone - resources['stone'])/min(buildings['Шахта']['ppl'],buildings['Склад']['ppl']))
        else: timetoStone = 0

        #print("timetoGold: %d; timetoWood: %d; timetoStone: %d" % (timetoGold, timetoWood, timetoStone))

        #Закупаемся максимум до MIN_GOLD
        moneyToSpend = resources['gold'] - MIN_GOLD
        moneyToSpend = max(moneyToSpend,0)

        #print("Money to spend: %d" % moneyToSpend)

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

        #print("woodToBuy: %d; stoneToBuy: %d" % (woodToBuy, stoneToBuy))

        #Проверяем что закупаем не слишком много
        if gold > MIN_GOLD:
            lastPeriod = int((gold - MIN_GOLD)/builder.getIncom('Ратуша'))
            maxWood = wood - lastPeriod * min(buildings['Лесопилка']['ppl'],buildings['Склад']['ppl'])
            maxWood = max(maxWood,0)
            maxStone = stone - lastPeriod * min(buildings['Шахта']['ppl'],buildings['Склад']['ppl'])
            maxStone = max(maxStone,0)

        if woodToBuy > 0 and resources['wood'] + woodToBuy > maxWood: woodToBuy = maxWood - resources['wood']
        woodToBuy = max(woodToBuy,0)
        if stoneToBuy > 0 and resources['stone'] + stoneToBuy > maxStone: stoneToBuy = maxStone - resources['stone']
        stoneToBuy = max(stoneToBuy,0)
            
        #print("maxWood: %d; woodToBuy: %d; maxStone: %d; stoneToBuy: %d" % (maxWood, woodToBuy, maxStone, stoneToBuy))

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
