import math
import queue
import time
import re

AllBldngsNames = ('hall', 'storage', 'houses', 'sawmill', 'mine',
'farm', 'barracks', 'wall', 'trebuchet')

resources = {'gold' : 0, 'wood' : 0, 'stone' : 0, 'food' : 0, 'time' : None}

buildings = {'hall' : {'lvl' : 0}, 'storage' : {'lvl' : 0, 'ppl' : 0}, 'houses' : {'lvl' : 0, 'ppl' : 0},
	'sawmill' : {'lvl' : 0, 'ppl' : 0}, 'mine' : {'lvl' : 0, 'ppl' : 0}, 'farm' : {'lvl' : 0, 'ppl' : 0}}

war_bldngs = {'barracks' : {'lvl' : 0, 'ppl' : 0}, 'wall' : {'lvl' : 0, 'ppl' : 0}, 'trebuchet'  : {'lvl' : 0, 'ppl' : 0}}

costCoef = {'hall' : (500, 200, 200), 'storage' : (200, 100, 100), 'houses' : (200, 100, 100),
	'sawmill' : (100, 50, 50), 'mine' : (100, 50, 50), 'farm' : (100, 50, 50),
	'barracks' : (200, 100, 100), 'wall' : (5000, 500, 1500), 'trebuchet'  : (8000, 1000, 300)}

que = queue.Queue()

#Проверка что ресурсов хватает на апгрейд
def isResEnough(building):
    global resources

    cost = getUpgrCost(building)
    overGold = resources['gold'] - cost['gold']

    #Мы не продаем ресурсы - а только покупаем
    if overGold >= 0:
        needWood = cost['wood'] - resources['wood']
        if needWood < 0: needWood = 0
        needStone = cost['stone'] - resources['stone']
        if needStone < 0: needStone = 0
        if overGold - needWood*2 - needStone*2 >= 0: return True
    else: return False

#Проверка что надо закупать лес или камни для апгрейда
def isResBuyingNeed(building):
    global resources
    cost = getUpgrCost(building)
    if cost['wood'] > resources['wood'] or cost['stone'] > resources['stone']: return True
    else: return False
    

#Проверка уровня склада на возможность апгрейда
def isStorEnough(building):
    global buildings
    if buildings['storage']['lvl'] >= getStorReq(building): return True
    else: return False

#Необходимый уровень склада для апгрейда на lvlsUp уровней
def getStorReq(building, lvlsUp=1):
    global buildings
    preTargetLvl = buildings[building]['lvl'] + lvlsUp - 1
    return math.ceil(math.sqrt(max(costCoef[building][1:3]) * (preTargetLvl ** 2 + 3 * preTargetLvl + 2)/100 + 100) - 10)
    

#Стоимость апгрейда на lvlsUp уровней
def getUpgrCost(building, lvlsUp=1):
    global buildings
    global costCoef
    #Текущий уровень здания
    srcLvl = buildings[building]['lvl']
    #Уровень ДО которого считаем стоимость апгрейда
    dstLvl = srcLvl + lvlsUp
    #Определяем два члена полинома, в зависимости от текущего(Poly2) и целевого уровней(Poly1)
    #Sn, Sm - частичныя суммы ряда от 0 до n и от 0 до m. Тогда Snm = Sm - Sn - сумма ряда от n до m
    Sm = dstLvl * (dstLvl-1) * ((2*dstLvl+8)/6 + 2/dstLvl)
    #Если текущий уровень - 0, то -Sn/2 должен обращаться в 1, тогда Sn = -2
    if srcLvl == 0: Sn = -2
    else: Sn = srcLvl * (srcLvl-1) * ((2*srcLvl+8)/6 + 2/srcLvl)
    gold = int(costCoef[building][0] * (Sm - Sn) / 2)
    wood = int(costCoef[building][1] * (Sm - Sn) / 2)
    stone = int(costCoef[building][2] * (Sm - Sn) / 2)
    return {'gold' : gold, 'wood' : wood, 'stone' : stone, 'total' : gold + wood * 2 + stone * 2}

#Максимальное количество людей в строении
def getMaxPpl(building):
    global buildings
    if building == 'storage' or building == 'sawmill' or building == 'mine' or building == 'farm' or building == 'wall': return buildings[building]['lvl'] * 10
    elif building == 'houses': return buildings[building]['lvl'] * 20
    elif building == 'barracks': return buildings[building]['lvl'] * 40
    elif building == 'trebuchet': return math.ceil(buildings[building]['lvl'] / 5)
    else: return None

#окупаемость
def getROI(building):
    #добавить вычисление ROI для одновременного аппа нескольких зданий
    global buildings
    incomUp = getIncUp(building)
    storLvlsUp = getStorReq(building) - buildings['storage']['lvl']
    #Для постройки необходимо апнуть склад на storLvlsUp уровней
    if storLvlsUp > 0:
        totalUpgrCost = getUpgrCost(building)['total'] + getUpgrCost('storage', stotLvlsUp)['total']
    #Ап склада не требуется
    else: totalUpgrCost = getUpgrCost(building)['total']
    if incomUp > 0: return totalUpgrCost/incomUp
    #Если доход меньше или равен 0, то окупаемость - бесконечность
    else: return math.inf

#прирост дохода при апгрейде
def getIncUp(building):
    global buildings
    if building == 'hall': return buildings['houses']['lvl'] * 2
    elif building == 'houses':
        if min(buildings['farm']['lvl'],buildings['storage']['lvl']) > buildings['houses']['lvl']: consumptFarm = 5
        else: consumptFarm = 20
        return 10 + buildings['hall']['lvl'] * 2 - consumptFarm
    elif building == 'farm':
        if buildings['farm']['lvl'] >= buildings['storage']['lvl']: return 0
        else:
            if buildings['farm']['lvl'] >= buildings['houses']['lvl']: return 5
            else: return 20
    elif building == 'sawmill' or building == 'mine':
        if buildings[building]['lvl'] < buildings['storage']['lvl']: return 20
        else: return 0
    elif building == 'storage':
        incomUp = 0
        if buildings['storage']['lvl'] < buildings['farm']['lvl']:
            if buildings['storage']['lvl'] < buildings['houses']['lvl']: incomUp += 20
            else: incomUp += 5
        if buildings['storage']['lvl'] < buildings['sawmill']['lvl']: incomUp += 20
        if buildings['storage']['lvl'] < buildings['mine']['lvl']: incomUp += 20
        return incomUp
    else: return 0

#Расчет дохода по зданию
def getIncom(building):
    #Дома и ратуша создают общий доход
    if building == 'houses' or building == 'hall':
        return buildings['houses']['lvl'] * 10 + buildings['houses']['lvl'] * buildings['hall']['lvl'] * 2
    elif building == 'farm':
        overFarm = min(buildings['farm']['lvl'],buildings['storage']['lvl']) - buildings['houses']['lvl']
        #Ферма производит избыток еды
        if overFarm > 0: return overFarm * 5
        #Производство еды в дефиците
        else: return overFarm * 20
    elif building == 'sawmill' or building == 'mine':
        return min(buildings[building]['lvl'],buildings['storage']['lvl']) * 20
    else: return 0

#Расчет общего дохода
def getTotalIncom():
    return getIncom('hall') + getIncom('farm') + getIncom('sawmill') + getIncom('mine')

#Следующее здание для апгрейда
def getNextUpgrBld():
    global buildings

    #Первые три постройки Дома, Склад, Ферма
    if buildings['houses']['lvl'] == 0: return 'houses'
    if buildings['storage']['lvl'] == 0: return 'storage'
    if buildings['farm']['lvl'] == 0: return 'farm'

    #Дальше считаем по окупаемости

    #Дом+Ферма
    incomUp = 10 + buildings['hall']['lvl']*2
    #Если склада не хватает, вычитаем из дохода расходы на еду
    if buildings['storage']['lvl'] <= buildings['farm']['lvl']: incomUp -= 20
    if incomUp <= 0: hausfarm = math.inf
    else: hausfarm = (getUpgrCost('houses')['total'] + getUpgrCost('farm')['total'])/incomUp

    #Дом+Ратуша
    storLvlUp = max(getStorReq('houses'),getStorReq('hall')) - buildings['storage']['lvl']
    incomUp = getIncUp('houses') + (buildings['houses']['lvl'] + 1)*2
    upgrCost = getUpgrCost('houses')['total']+getUpgrCost('hall')['total']
    #Если необходим ап складов, то считаем
    if storLvlUp > 0: upgrCost += getUpgrCost('storage',storLvlUp)['total']
    if incomUp <= 0: haushall = math.inf
    else: haushall = upgrCost/incomUp
            
    #Склад+Лесопилка+Шахта
    skld1 = (getUpgrCost('storage')['total'] + getUpgrCost('sawmill')['total'] + getUpgrCost('mine')['total'])/40
    #Склад+Лесопилка+Шахта+Ферма
    if buildings['farm']['lvl'] + 1 >=  buildings['houses']['lvl']:
        skld2 = (getUpgrCost('storage')['total'] + getUpgrCost('sawmill')['total'] + getUpgrCost('mine')['total'] + getUpgrCost('farm')['total'])/45
    else:
        skld2 = (getUpgrCost('storage')['total'] + getUpgrCost('sawmill')['total'] + getUpgrCost('mine')['total'] + getUpgrCost('farm')['total'])/60
    #Склад+Дома+Ферма
    skld3 = (getUpgrCost('storage')['total'] + getUpgrCost('houses')['total'] + getUpgrCost('farm')['total'])/(10 + buildings['hall']['lvl']*2)

    storROI = min(skld1, skld2, skld3, getROI('storage')) #минимум из всех вариантов со складом
    hallROI = getROI('hall')
    hausROI = getROI('houses')
    farmROI = getROI('farm')
    sawmROI = getROI('sawmill')
    mineROI = getROI('mine')

    minROI = min(storROI, hallROI, hausROI, farmROI, sawmROI, mineROI, haushall, hausfarm)

    #Для Дома+Ратуша выбираем то что выгодней
    if minROI == haushall:
        if hausROI == min(hausROI, hallROI): hausROI = minROI
        else: hallROI = minROI
    #Или для Дома+Ферма выбираем то что выгодней
    elif minROI == hausfarm:
        if hausROI == min(hausROI, farmROI): hausROI = minROI
        else: farmROI = minROI


    if minROI == storROI: return 'storage'
    elif minROI == hallROI:
        if isStorEnough('hall'): return 'hall'
        else: return 'storage'
    elif minROI == hausROI:
        if isStorEnough('houses'): return 'houses'
        else: return 'storage'
    elif minROI == farmROI:
        if isStorEnough('farm'): return 'farm'
        else: return 'storage'
    elif minROI == sawmROI:
        if isStorEnough('sawmill'): return 'sawmill'
        else: return 'storage'
    elif minROI == mineROI:
        if isStorEnough('mine'): return 'mine'
        else: return 'storage'
    
    #Что-то пошло не так и мы оказались здесь
    return None
    
#Проапгрейдить здание
def doUpgrade(building=getNextUpgrBld()):
    global que

    #TODO: Если ресурсы обновлялись больше минуты назад, делаем "наверх", ставим флаг doUpgrade
    # и делаем апгрейд в парсере сообщений при обновлении

    if isResEnough(building):
        if isResBuyingNeed(building):
            doBuyReses(building,True)
            return
        else:
            que.put('Наверх')
            if building == 'trebuchet':
                que.put('Мастерская')
                que.put('Требушет')
            else:
                que.put('Постройки')
                if building == 'storage':
                    que.put('Склад')
                elif building == 'hall':
                    que.put('Ратуша')
                elif building == 'houses':
                    que.put('Дома')
                elif building == 'farm':
                    que.put('Ферма')
                elif building == 'sawmill':
                    que.put('Лесопилка')
                elif building == 'mine':
                    que.put('Шахта')
                elif building == 'barracks':
                    que.put('Казармы')
                elif building == 'wall':
                    que.put('Стена')
            que.put('Улучшить')
    else: print('ресурсов на постройку недостаточно')

#Закупить ресурсы
def doBuyReses(building=getNextUpgrBld(),doUpgr=False):
    global que
    #Закупаем ресурсы
    cost = getUpgrCost(building)
    que.put('Наверх')
    que.put('Торговля')
    que.put('Купить')

    que.put('Дерево')
    que.put(cost['wood'] - resources['wood'])
    #В предположении что закупка состится успешно:
    resources['wood'] = cost['wood']

    que.put('Назад')
    que.put('Камень')
    que.put(cost['stone'] - resources['stone'])
    #В предположении что закупка состится успешно:
    resources['stone'] = cost['stone']

    #И делаем апгрейд если надо
    if doUpgr: doUpgrade(building)
    #TODO: устанавливаем флаг doUpgrade и делаем апгрейд в парсере сообщений
    #В таком случае возможно срабатывание раньше времени и повторная закупка ресурсов
    #Вариант: постановка в очередь маркера окончания закупки

#парсер сообщений от бота
def msgParser(text):
    global resources
    global buildings
    global war_bldngs

    res = re.search(r"""(?:Жители\s+(\d+).\n)?
                        (?:Армия\s+(\d+).\n)?
                           Золото\s+(\d+).\n
                           Дерево\s+(\d+).\n
                           Камень\s+(\d+).\n
                           Еда\s+(\d+).""", text)
    if res > 0:
        resources['gold'] = res.group(2)
        resources['wood'] = res.group(3)
        resources['stone'] = res.group(4)
        resources['food'] = res.group(5)
        resources['time'] = int(time.time()/60)

    bld = (r"""^Постройки\n
                   \n
                  (?:\U0001f3e4\s+(\d+).+\n)?
                  (?:\U0001f3da\s+(\d+).+\s+(\d+)/.+\n)?
                  (?:\U0001f3d8\s+(\d+).+\s+(\d+)/.+\n)?
                  (?:\U0001f33b\s+(\d+).+\s+(\d+)/.+\n)?
                  (?:\U0001f332\s+(\d+).+\s+(\d+)/.+\n)?
                  (?:\u26cf\s+(\d+).+\s+(\d+)/.+\n)?
                  (?:\U0001f6e1\s+(\d+).+\s+(\d+)/.+\n)?
                  (?:\U0001f3f0\s+(\d+).+\s+(\d+)/.+\n)?
                  \n
                  Что будем строить\?$""", text)
    if bld.group(0): buildings['hall']['lvl'] = bld.group(0)
    if bld.group(1): buildings['storage']['lvl'] = bld.group(1)
    if bld.group(2): buildings['houses']['lvl'] = bld.group(2)
    if bld.group(3): buildings['farm']['lvl'] = bld.group(3)
    if bld.group(4): buildings['sawmill']['lvl'] = bld.group(4)
    if bld.group(5): buildings['mine']['lvl'] = bld.group(5)

    if bld.group(6): war_bldngs['barracks']['lvl'] = bld.group(6)
    if bld.group(7): war_bldngs['wall']['lvl'] = bld.group(7)
