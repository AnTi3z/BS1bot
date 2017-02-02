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
    #Необходимое количество еды
    if foodNeed < 0: foodNeed = 0
    #Если золота не хватает - покупаем еду на все деньги
    elif foodNeed > resources['gold'] / 2:
        foodNeed = resources['gold'] / 2
        foodReserv = foodNeed + resources['food']

    #Покупка
    doBuyReses(food=int(foodNeed))

    #Корректировка времени на которое расчитан запас еды
    if foodConsum * hrsReserv * 60 > foodReserv: hrsReserv = foodReserv / (foodConsum * 60)

    #Следующая покупка через половину времени на которое у нас запас
    if AUTOFEED: timer.setFeedTimer(int(hrsReserv*60/2))
