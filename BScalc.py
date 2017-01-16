import math
import queue

AllBldngsNames = ('hall', 'storage', 'houses', 'sawmill', 'mine',
'farm', 'barracks', 'wall', 'trebuchet')

resources = {'gold' : 0, 'wood' : 0, 'stone' : 0, 'food' : 0, 'time' : None}

buildings = {'hall' : {'lvl' : 0}, 'storage' : {'lvl' : 0, 'ppl' : 0}, 'houses' : {'lvl' : 0, 'ppl' : 0},
	'sawmill' : {'lvl' : 4, 'ppl' : 0}, 'mine' : {'lvl' : 0, 'ppl' : 0}, 'farm' : {'lvl' : 0, 'ppl' : 0}}

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
    global buildings
    incomUp = getIncUp(building)
    storLvlsUp = getStorReq(building) - buildings['storage']['lvl']
    #Для постройки необходимо апнуть склад на storLvlsUp уровней
    if getStorReq(building) > buildings['storage']['lvl']:
        storLvlsUp = getStorReq(building) - buildings['storage']['lvl']
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
    #заглушка для теста
    return 'storage'
    pass

#Проапгрейдить здание
def doUpgrade(building=getNextUpgrBld()):
    global que
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

#парсер сообщений от бота
def msgParser(text):
    global resources
    global buildings
    pass
