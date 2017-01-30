from .globalobjs import *
from .tools import doBuyReses
from . import timer

def doBuyFood():
    hrsReserv = FOOD_RESERV_TIME

    foodConsum = (buildings['Дома']['lvl'] - min(buildings['Склад']['lvl'],buildings['Ферма']['lvl'])) * 10
    foodReserv = foodConsum * hrsReserv * 60
    storCapacity = (buildings['Склад']['lvl']*50 + 1000) * buildings['Склад']['lvl']
    foodReserv = min(storCapacity, foodReserv)
    foodNeed = foodReserv - resources['food']
    if foodNeed < 0: foodNeed = 0

    doBuyReses(food=foodNeed)

    if foodConsum * hrsReserv * 60 < foodReserv/2: hrsReserv = foodReserv / (foodConsum * 60)

    if AUTOFEED: timer.setFeedTimer(int(hrsReserv*60/2))
