import math
import time

from . import globalobjs
from .globalobjs import *
from . import tools
from . import queues
from . import timer

#Проверка что ресурсов хватает на апгрейд
def isResEnough(building):
    if getResNeed(building)['total'] == 0: return True
    else: return False

#Необходимые для апгрейда ресурсы
def getResNeed(building):
    cost = getUpgrCost(building)
    needGold = cost['gold'] - resources['gold']
    needGold = max(needGold,0)
    needWood = cost['wood'] - resources['wood']
    needWood = max(needWood,0)
    needStone = cost['stone'] - resources['stone']
    needStone = max(needStone,0)
    total = needGold + needWood * 2 + needStone * 2
    total = max(total,0)
    return {'gold' : needGold, 'wood' : needWood, 'stone' : needStone, 'total' : total}

#Проверка что надо закупать лес или камни для апгрейда
def isResBuyingNeed(building):
    cost = getUpgrCost(building)
    if cost['wood'] > resources['wood'] or cost['stone'] > resources['stone']: return True
    else: return False


#Проверка уровня склада на возможность апгрейда
def isStorEnough(building):
    if buildings['Склад']['lvl'] >= getStorReq(building): return True
    else: return False


#Необходимый уровень склада для апгрейда на lvlsUp уровней
def getStorReq(building, lvlsUp=1):
    preTargetLvl = buildings[building]['lvl'] + lvlsUp - 1
    return math.ceil(math.sqrt(max(COST_COEF[building][1:3]) * (preTargetLvl ** 2 + 3 * preTargetLvl + 2)/100 + 100) - 10)


#Стоимость апгрейда на lvlsUp уровней
def getUpgrCost(building, lvlsUp=1):
    #Текущий уровень здания
    srcLvl = buildings[building]['lvl']
    #Уровень ДО которого считаем стоимость апгрейда
    dstLvl = srcLvl + lvlsUp
    #Определяем два члена полинома, в зависимости от текущего(Poly2) и целевого уровней(Poly1)
    #Sn, Sm - частичныя суммы ряда от 0 до n и от 0 до m. Тогда Snm = Sm - Sn - сумма ряда от n до m
    Sm = round(dstLvl * (dstLvl-1) * ((2*dstLvl+8)/6 + 2/dstLvl))
    #Если текущий уровень - 0, то -Sn/2 должен обращаться в 1, тогда Sn = -2
    if srcLvl == 0: Sn = -2
    else: Sn = round(srcLvl * (srcLvl-1) * ((2*srcLvl+8)/6 + 2/srcLvl))
    gold = round(COST_COEF[building][0] * (Sm - Sn) / 2)
    wood = round(COST_COEF[building][1] * (Sm - Sn) / 2)
    stone = round(COST_COEF[building][2] * (Sm - Sn) / 2)
    return {'gold' : gold, 'wood' : wood, 'stone' : stone, 'total' : gold + wood * 2 + stone * 2}


#Максимальное количество людей в строении
def getMaxPpl(building):
    if building == 'Склад' or building == 'Лесопилка' or building == 'Шахта' or building == 'Ферма' or building == 'Стена': return buildings[building]['lvl'] * 10
    elif building == 'Дома': return buildings[building]['lvl'] * 20
    elif building == 'Казармы': return buildings[building]['lvl'] * 40
    elif building == 'Требушет': return math.ceil(buildings[building]['lvl'] / 5)
    else: return None


#окупаемость
def getROI(building):
    #добавить вычисление ROI для одновременного аппа нескольких зданий
    incomUp = getIncUp(building)
    storLvlsUp = getStorReq(building) - buildings['Склад']['lvl']
    #Для постройки необходимо апнуть склад на storLvlsUp уровней
    if storLvlsUp > 0:
        totalUpgrCost = getUpgrCost(building)['total'] + getUpgrCost('Склад', storLvlsUp)['total']
    #Ап склада не требуется
    else: totalUpgrCost = getUpgrCost(building)['total']
    if incomUp > 0: return totalUpgrCost/incomUp
    #Если доход меньше или равен 0, то окупаемость - бесконечность
    else: return math.inf


#прирост дохода при апгрейде
def getIncUp(building):
    if building == 'Ратуша': return buildings['Дома']['lvl'] * 2
    elif building == 'Дома':
        if min(buildings['Ферма']['lvl'],buildings['Склад']['lvl']) > buildings['Дома']['lvl']: consumptFarm = 5
        else: consumptFarm = 20
        return 10 + buildings['Ратуша']['lvl'] * 2 - consumptFarm
    elif building == 'Ферма':
        if buildings['Ферма']['lvl'] >= buildings['Склад']['lvl']: return 0
        else:
            if buildings['Ферма']['lvl'] >= buildings['Дома']['lvl']: return 5
            else: return 20
    elif building == 'Лесопилка' or building == 'Шахта':
        if buildings[building]['lvl'] < buildings['Склад']['lvl']: return 20
        else: return 0
    elif building == 'Склад':
        incomUp = 0
        if buildings['Склад']['lvl'] < buildings['Ферма']['lvl']:
            if buildings['Склад']['lvl'] < buildings['Дома']['lvl']: incomUp += 20
            else: incomUp += 5
        if buildings['Склад']['lvl'] < buildings['Лесопилка']['lvl']: incomUp += 20
        if buildings['Склад']['lvl'] < buildings['Шахта']['lvl']: incomUp += 20
        return incomUp
    else: return 0

#Расчет производительности производства
def getProduct(building):
    if building == 'Лесопилка' or building == 'Шахта' or building == 'ферма':
        return min(buildings[building]['ppl'],buildings['Склад']['ppl'])
    else: return 0

#Расчет дохода по зданию
def getIncom(building):
    #Дома и ратуша создают общий доход
    if building == 'Дома' or building == 'Ратуша':
        return buildings['Дома']['lvl'] * 10 + buildings['Дома']['lvl'] * buildings['Ратуша']['lvl'] * 2
    elif building == 'Ферма':
        overFarm = min(buildings['Ферма']['lvl'],buildings['Склад']['lvl']) - buildings['Дома']['lvl']
        #Ферма производит избыток еды
        if overFarm > 0: return overFarm * 5
        #Производство еды в дефиците
        else: return overFarm * 20
    elif building == 'Лесопилка' or building == 'Шахта':
        return min(buildings[building]['lvl'],buildings['Склад']['lvl']) * 20
    else: return 0


#Расчет общего дохода
def getTotalIncom():
    return getIncom('Ратуша') + getIncom('Ферма') + getIncom('Лесопилка') + getIncom('Шахта')


#Следующее здание для апгрейда
def getNextUpgrBld():
    #Первые три постройки Дома, Склад, Ферма
    if buildings['Дома']['lvl'] == 0: return 'Дома'
    if buildings['Склад']['lvl'] == 0: return 'Склад'
    if buildings['Ферма']['lvl'] == 0: return 'Ферма'

    #Дальше считаем по окупаемости

    #Дом+Ферма
    storLvlUp = max(getStorReq('Дома'),getStorReq('Ферма')) - buildings['Склад']['lvl']
    incomUp = 10 + buildings['Ратуша']['lvl']*2
    #Если склада не хватает, вычитаем из дохода расходы на еду
    if buildings['Склад']['lvl'] <= buildings['Ферма']['lvl']: incomUp -= 20
    upgrCost = getUpgrCost('Дома')['total'] + getUpgrCost('Ферма')['total']
    #Если необходим ап складов, то считаем
    if storLvlUp > 0: upgrCost += getUpgrCost('Склад',storLvlUp)['total']
    if incomUp <= 0: hausfarm = math.inf
    else: hausfarm = upgrCost/incomUp

    #Дом+Ратуша
    storLvlUp = max(getStorReq('Дома'),getStorReq('Ратуша')) - buildings['Склад']['lvl']
    incomUp = getIncUp('Дома') + (buildings['Дома']['lvl'] + 1)*2
    upgrCost = getUpgrCost('Дома')['total']+getUpgrCost('Ратуша')['total']
    #Если необходим ап складов, то считаем
    if storLvlUp > 0: upgrCost += getUpgrCost('Склад',storLvlUp)['total']
    if incomUp <= 0: haushall = math.inf
    else: haushall = upgrCost/incomUp

    #Склад+Лесопилка+Шахта
    skld1 = (getUpgrCost('Склад')['total'] + getUpgrCost('Лесопилка')['total'] + getUpgrCost('Шахта')['total'])/40
    #Склад+Лесопилка+Шахта+Ферма
    if buildings['Ферма']['lvl'] + 1 >=  buildings['Дома']['lvl']:
        skld2 = (getUpgrCost('Склад')['total'] + getUpgrCost('Лесопилка')['total'] + getUpgrCost('Шахта')['total'] + getUpgrCost('Ферма')['total'])/45
    else:
        skld2 = (getUpgrCost('Склад')['total'] + getUpgrCost('Лесопилка')['total'] + getUpgrCost('Шахта')['total'] + getUpgrCost('Ферма')['total'])/60
    #Склад+Дома+Ферма
    skld3 = (getUpgrCost('Склад')['total'] + getUpgrCost('Дома')['total'] + getUpgrCost('Ферма')['total'])/(10 + buildings['Ратуша']['lvl']*2)

    storROI = min(skld1, skld2, skld3, getROI('Склад')) #минимум из всех вариантов со складом
    hallROI = getROI('Ратуша')
    hausROI = getROI('Дома')
    farmROI = getROI('Ферма')
    sawmROI = getROI('Лесопилка')
    mineROI = getROI('Шахта')

    minROI = min(storROI, hallROI, hausROI, farmROI, sawmROI, mineROI, haushall, hausfarm)

    #Для Дома+Ратуша выбираем то что выгодней
    if minROI == haushall:
        if hausROI == min(hausROI, hallROI): hausROI = minROI
        else: hallROI = minROI
    #Или для Дома+Ферма выбираем то что выгодней
    elif minROI == hausfarm:
        if hausROI == min(hausROI, farmROI): hausROI = minROI
        else: farmROI = minROI

    if minROI == storROI: return 'Склад'
    elif minROI == hallROI:
        if isStorEnough('Ратуша'): return 'Ратуша'
        else: return 'Склад'
    elif minROI == hausROI:
        if isStorEnough('Дома'): return 'Дома'
        else: return 'Склад'
    elif minROI == farmROI:
        if isStorEnough('Ферма'): return 'Ферма'
        else: return 'Склад'
    elif minROI == sawmROI:
        if isStorEnough('Лесопилка'): return 'Лесопилка'
        else: return 'Склад'
    elif minROI == mineROI:
        if isStorEnough('Шахта'): return 'Шахта'
        else: return 'Склад'

    #Что-то пошло не так и мы оказались здесь
    return None


#Проапгрейдить здание
def doUpgrade(building=None):
    building = building or getNextUpgrBld()

    if resources['time'] < int(time.time()/60):
        queues.queThrdsLock.acquire()
        queues.msgQueAdd('Наверх')
        queues.queThrdsLock.release()
        #Запустить таймер на 5 секунд или time.sleep(5)
        queues.cmdQueAdd(('build', building))
        return

    if isResEnough(building):
        if isResBuyingNeed(building):
            cost = getUpgrCost(building)
            woodNeed = cost['wood'] - resources['wood']
            woodNeed = max(woodNeed, 0)
            stoneNeed = cost['stone'] - resources['stone']
            stoneNeed = max(stoneNeed,0)
            tools.doBuyReses(wood=woodNeed,stone=stoneNeed)
            queues.cmdQueAdd(('build', building))
            return
        else:
            queues.queThrdsLock.acquire()
            queues.msgQueAdd('Наверх')
            if building == 'Требушет':
                queues.msgQueAdd('Мастерская')
            else:
                queues.msgQueAdd('Постройки')
            queues.msgQueAdd(building)
            queues.msgQueAdd('Улучшить')
            #Отправляем в постройку людей(добавить проверки)
            if building != 'Ратуша' and building != 'Дома':
                if building == 'Казармы' or building == 'Стена': queues.msgQueAdd('Обучить')
                else: queues.msgQueAdd('Отправить')
                if building == 'Казармы': queues.msgQueAdd('40')
                elif building == 'Требушет': queues.msgQueAdd('1')
                else: queues.msgQueAdd('10')
            queues.msgQueAdd('Наверх')
            queues.queThrdsLock.release()
            globalobjs.SendInfo_cb('\u26a0 Апгрейд здания: %s' % building)
            if AUTOBUILD: queues.cmdQueAdd(('build',))
    else:
        bldCost = getUpgrCost(building)
        needTotal = getResNeed(building)['total']
        #Придумать обработчик при getTotalIncom = 0
        lefttime = math.ceil(needTotal / getTotalIncom())
        globalobjs.SendInfo_cb('\U0001f4ac Ресурсов на постройку %s недостаточно.\nНедостает %d\U0001f4b0\nДо постройки %d\U0001f553 минут.' % (building, needTotal, lefttime))
        #Запустить таймер через расчетное время (+1 минута)
        timer.setUpgrTimer(lefttime+1, building)
        #Запустить таймер на переодическую закупку ресурсов (чтоб не копить золото)
        tools.doTargetReses(gold=bldCost['gold'],wood=bldCost['wood'],stone=bldCost['stone'])

#Отправить в здание людей
def doSendPpl(building, ppl):
    if ppl <= 0 or building == 'Ратуша' or building == 'Дома': return
    
    queues.queThrdsLock.acquire()
    queues.msgQueAdd('Наверх')
    if building == 'Требушет':
        queues.msgQueAdd('Мастерская')
    else:
        queues.msgQueAdd('Постройки')
    queues.msgQueAdd(building)
    #Отправляем в постройку людей(добавить проверки)
    if building == 'Казармы' or building == 'Стена': queues.msgQueAdd('Обучить')
    else: queues.msgQueAdd('Отправить')
    queues.msgQueAdd(str(ppl))
    #queues.msgQueAdd('Наверх')
    queues.queThrdsLock.release()
    globalobjs.SendInfo_cb('\u26a0 Отправляем %d человек в %s' % (ppl,building))

def doRetPpl(building, ppl):
    if ppl <= 0 or building == 'Ратуша' or building == 'Дома': return
    
    queues.queThrdsLock.acquire()
    queues.msgQueAdd('Наверх')
    if building == 'Требушет':
        queues.msgQueAdd('Мастерская')
    else:
        queues.msgQueAdd('Постройки')
    queues.msgQueAdd(building)
    #Заюираем из постройки людей(добавить проверки)
    queues.msgQueAdd('Отозвать')
    queues.msgQueAdd(str(ppl))
    #queues.msgQueAdd('Наверх')
    queues.queThrdsLock.release()
    globalobjs.SendInfo_cb('\u26a0 Забираем %d человек из %s' % (ppl,building))
