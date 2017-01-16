import math

AllBldngsNames = ('hall', 'storage', 'houses', 'sawmill', 'mine',
'farm', 'barracks', 'wall', 'trebuchet')

resources = {'gold' : 0, 'wood' : 0, 'stone' : 0, 'food' : 0, 'time' : None}

buildings = {'hall' : {'lvl' : 0}, 'storage' : {'lvl' : 0, 'ppl' : 0}, 'houses' : {'lvl' : 0, 'ppl' : 0},
	'sawmill' : {'lvl' : 0, 'ppl' : 0}, 'mine' : {'lvl' : 0, 'ppl' : 0}, 'farm' : {'lvl' : 0, 'ppl' : 0}}

war_bldngs = {'barracks' : {'lvl' : 0, 'ppl' : 0}, 'wall' : {'lvl' : 0, 'ppl' : 0}, 'trebuchet'  : {'lvl' : 0, 'ppl' : 0}}

costCoef = {'hall' : (500, 200, 200), 'storage' : (200, 100, 100), 'houses' : (200, 100, 100),
	'sawmill' : (100, 50, 50), 'mine' : (100, 50, 50), 'farm' : (100, 50, 50),
	'barracks' : (200, 100, 100), 'wall' : (5000, 500, 1500), 'trebuchet'  : (8000, 1000, 300)}


#Проверка что ресурсов хватает на апгрейд
def isResEnough(building):
    global resources
    cost = getUpgrCost(building)
    overGold = resources['gold'] - cost['gold']
    #Мы не продаем ресурсы - а только покупаем
    if overGold >= 0: needWood = cost['wood'] - resources['wood']
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
    gold = int(costCoef[building][0] * (buildings[building]['lvl'] ** 2 + buildings[building]['lvl'] * 3 + 2) / 2)
    wood = int(costCoef[building][1] * (buildings[building]['lvl'] ** 2 + buildings[building]['lvl'] * 3 + 2) / 2)
    stone = int(costCoef[building][2] * (buildings[building]['lvl'] ** 2 + buildings[building]['lvl'] * 3 + 2) / 2)
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
    incomUp = getIncUp(building)
    if incomUp > 0: return = getUpgrCost(building)/incomUp
    else: return math.inf

#прирост дохода при апгрейде
def getIncUp(building):
    global buildings
    if building == 'hall': return buildings['hall']['lvl'] * 10
    elif building == 'houses':
        if min(buildings['farm']['lvl'],buildings['storage']['lvl']) > buildings['houses']['lvl']: consumptFarm = 5
        else: consumptFarm = 20
        return 10 + buildings['houses']['lvl'] * 2 - consumptFarm
    elif building == 'farm':
        if buildings['farm']['lvl'] >= buildings['storage']['lvl']: return 0
        else:
            if buildings['farm']['lvl'] >= buildings['houses']['lvl']: return 5
            else: return 20
    elif building == 'sawmill' or building == 'mine':
        if buildings[building]['lvl'] < buildings['storage']['lvl']: return 20
        else: return 0
    else: return 0

def getIncom(building):
    pass

def getTotalIncom

#парсер сообщений от бота
def msgParser(text):
    pass
