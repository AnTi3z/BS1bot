import math
import queue

AllBldngsNames = ('hall', 'storage', 'houses', 'sawmill', 'mine',
'farm', 'barracks', 'wall', 'trebuchet')

resources = {'gold' : 0, 'wood' : 0, 'stone' : 0, 'food' : 0, 'time' : None}

buildings = {'hall' : {'lvl' : 1}, 'storage' : {'lvl' : 4, 'ppl' : 0}, 'houses' : {'lvl' : 2, 'ppl' : 0},
	'sawmill' : {'lvl' : 4, 'ppl' : 0}, 'mine' : {'lvl' : 4, 'ppl' : 0}, 'farm' : {'lvl' : 3, 'ppl' : 0}}

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
        if needWood < 0:
            needWood = 0
            needStone = cost['stone'] - resources['stone']
            if needStone < 0: needStone = 0
            if overGold - needWood*2 - needStone*2 >= 0: return True
    return False

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
    #Уровень ДО которого считаем стоимость апгрейда
    dstLvl = buildings[building]['lvl'] + lvlsUp
    #Определяем два члена полинома, в зависимости от текущего(Poly2) и целевого уровней(Poly1)
    Poly1 = dstLvl * (dstLvl-1) * ((2*dstLvl+8)/6 + 2/dstLvl)
    if buildings[building]['lvl'] == 0: Poly2 = -2
    else: Poly2 = buildings[building]['lvl'] * (buildings[building]['lvl']-1) * ((2*buildings[building]['lvl']+8)/6 + 2/buildings[building]['lvl'])
    gold = int(costCoef[building][0] * (Poly1 - Poly2) / 2)
    wood = int(costCoef[building][1] * (Poly1 - Poly2) / 2)
    stone = int(costCoef[building][2] * (Poly1 - Poly2) / 2)
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
    storLvlsUp = getStorReq(building) - buildings['storage']
    #Для постройки необходимо апнуть склад на storLvlsUp уровней
    if getStorReq(building) > buildings['storage']['lvl']:
        storLvlsUp = getStorReq(building) - buildings['storage']['lvl']
        totalUpCost = getUpgrCost(building)['total'] + getUpgrCost('storage', stotLvlsUp)['total']
    #Ап склада не требуется
    else: totalUpCost = getUpgrCost(building)['total']
    if incomUp > 0: return totalUpCost/incomUp
    #Если доход меньше или равень 0, то окупаемость - бесконечность
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
    pass

#Расчет общего дохода
def getTotalIncom():
    pass

#Следующее здание для апгрейда
def getNextUpgrBld():
    #заглушка для теста
    return 'storage'
    pass

#Проапгрейдить здание
def doUpgrade(building=getNextUpgrBld()):
    global que
    if isResEnough(building):
        if isResBuyingNeed:
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
    #Закупаем ресурсы
    #И делаем апгрейд если надо
    if doUpgr: doUpgrade(building)

#парсер сообщений от бота
def msgParser(text):
    pass
