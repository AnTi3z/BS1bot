import re
import time
import logging

from .globalobjs import *
#from . import tools
from . import timer
from . import builder
from . import war

logger = logging.getLogger(__name__)

#парсер сообщений от бота
def msgParser(text):

    #Наверх и ...-Торговля
    res = re.search(r"(?:Жители\s+(\d+).\n)?(?:Армия\s+(\d+).\n)?Золото\s+(\d+).\nДерево\s+(\d+).\nКамень\s+(\d+).\nЕда\s+(\d+).", text)
    if res:
        if res.group(1): buildings['Дома']['ppl'] = int(res.group(1))
        if res.group(2): buildings['Казармы']['ppl'] = int(res.group(2))
        resources['gold'] = int(res.group(3))
        resources['wood'] = int(res.group(4))
        resources['stone'] = int(res.group(5))
        resources['food'] = int(res.group(6))
        resources['time'] = int(time.time()/60)
        logger.debug("res: %s" % str(res.groups()))
        return

    #...-Постройки
    blds = re.search(r"^Постройки\n\n(?:\U0001f3e4\s+(\d+).+\n)?(?:\U0001f3da\s+(\d+).+\s+(\d+)/.+\n)?(?:\U0001f3d8\s+(\d+).+\s+(\d+)/.+\n)?(?:\U0001f33b\s+(\d+).+\s+(\d+)/.+\n)?(?:\U0001f332\s+(\d+).+\s+(\d+)/.+\n)?(?:\u26cf\s+(\d+).+\s+(\d+)/.+\n)?(?:\U0001f6e1\s+(\d+).+\s+(\d+)/.+\n)?(?:\U0001f3f0\s+(\d+).+\s+(\d+)/.+\n)?\nЧто будем строить\?$", text)
    if blds:
        if blds.group(1): buildings['Ратуша']['lvl'] = int(blds.group(1))
        if blds.group(2): buildings['Склад']['lvl'] = int(blds.group(2)); buildings['Склад']['ppl'] = int(blds.group(3))
        if blds.group(4): buildings['Дома']['lvl'] = int(blds.group(4)); buildings['Дома']['ppl'] = int(blds.group(5))
        if blds.group(6): buildings['Ферма']['lvl'] = int(blds.group(6)); buildings['Ферма']['ppl'] = int(blds.group(7))
        if blds.group(8): buildings['Лесопилка']['lvl'] = int(blds.group(8)); buildings['Лесопилка']['ppl'] = int(blds.group(9))
        if blds.group(10): buildings['Шахта']['lvl'] = int(blds.group(10)); buildings['Шахта']['ppl'] = int(blds.group(11))
        if blds.group(12): buildings['Казармы']['lvl'] = int(blds.group(12)); buildings['Казармы']['ppl'] = int(blds.group(13))
        if blds.group(14): buildings['Стена']['lvl'] = int(blds.group(14)); buildings['Стена']['ppl'] = int(blds.group(15))
        buildings['time'] = int(time.time()/60)
        logger.debug("blds: %s" % str(blds.groups()))
        return

    #...-Постройки-Лесопилка,Шахта,Ферма,Склад,Казармы | ...-Мастерская-Требушет
    bld = re.search(r"^.(Лесопилка|Шахта|Ферма|Склад|Требушет|Казармы)\s*\n\nУровень\s+(\d+)\n(?:Рабочие|Армия)\s+(\d+).+?\n\n(?:Склад\s+(\d+))?.+?Золото\s+(\d+).\nЖители\s+(\d+).+", text, re.S)
    if bld:
        build = bld.group(1)

        buildings[build]['lvl'] = int(bld.group(2))
        buildings[build]['ppl'] = int(bld.group(3))
        if bld.group(4): buildings['Склад']['ppl'] = int(bld.group(4))
        resources['gold'] = int(bld.group(5))
        buildings['Дома']['ppl'] = int(bld.group(6))
        logger.debug("bld: %s" % str(bld.groups()))
        return

    #...-Постройки-Дома
    hous = re.search(r"^.Дома\s*\n\nУровень\s+(\d+)\nЖители\s+(\d+).+?Склад\s+(\d+).+", text, re.S)
    if hous:
        buildings['Дома']['lvl'] = int(hous.group(1))
        buildings['Дома']['ppl'] = int(hous.group(2))
        buildings['Склад']['ppl'] = int(hous.group(3))
        logger.debug("hous: %s" % str(hous.groups()))
        return

    #...-Постройки-Ратуша
    hall = re.search(r"^.Ратуша\s*\n\nУровень\s+(\d+)\nЗолото\s+(\d+).+", text, re.S)
    if hall:
        buildings['Ратуша']['lvl'] = int(hall.group(1))
        resources['gold'] = int(hall.group(2))
        logger.debug("hall: %s" % str(hall.groups()))
        return

    #...-Постройки-Стена
    wall = re.search(r"^.Стена\s+Уровень\s+(\d+)\nЛучники\s+(\d+).+Прочность\s+(\d+).+Золото\s+(\d+).\nЖители\s+(\d+).+", text, re.S)
    if wall:
        buildings['Стена']['lvl'] = int(wall.group(1))
        buildings['Стена']['ppl'] = int(wall.group(2))
        buildings['Стена']['str'] = int(wall.group(3))
        resources['gold'] = int(wall.group(4))
        buildings['Дома']['ppl'] = int(wall.group(5))
        logger.debug("wall: %s" % str(wall.groups()))
        return

    #...-Война
    batl = re.search(r"^Победы\s+\d+.\n(?:Карма\s+(\d+))?.+?\n\n(?:.Стена\s+\nПрочность\s+(\d+).+?\nЛучники\s+(\d+)\S+\n\n)?(?:.Требушет\s+\nРабочие\s+(\d+)\S+\n\n)?.+?Армия\s+(\d+).+Еда\s+(\d+)\S+?\n?(?:\nСледующая атака\s+(\d+)\sмин.)?(?:\nБез нападений\s+(\d+)\sмин.)?(\nПрод)?.*", text, re.S)
    if batl:
        if batl.group(1): pass #Карма
        if batl.group(2): buildings['Стена']['str'] = int(batl.group(2))
        if batl.group(3): buildings['Стена']['ppl'] = int(batl.group(3))
        if batl.group(4): buildings['Требушет']['ppl'] = int(batl.group(4))
        buildings['Казармы']['ppl'] = int(batl.group(5))
        resources['food'] = int(batl.group(6))
        if batl.group(7): war.cooldown = time.time() + 60*int(batl.group(7))
        else: war.cooldown = None
        if batl.group(8): war.imune = time.time() + 60*int(batl.group(8))
        else: war.imune = None
        war.battle = not (batl.group(9) == None)
        logger.debug("batl: %s" % str(batl.groups()))
        return

    #...-Война-Обучить
    army = re.search(r"^.Инфо\s+\n\n(?:.Казармы\s+(\d+).+\n?)?(?:.Стена\s+(\d+).+\n?)?(?:.Требушет\s+(\d+).+)?", text)
    if army:
        if army.group(1): buildings['Казармы']['ppl'] = int(army.group(1))
        if army.group(2): buildings['Стена']['ppl'] = int(army.group(2))
        if army.group(3): buildings['Требушет']['ppl'] = int(army.group(3))
        logger.debug("army: %s" % str(army.groups()))
        return

    #...-Мастерская
    treb = re.search(r"^Мастерская\n\n.Требушет\s+(\d+).+?(\d+).+", text)
    if treb:
        buildings['Требушет']['lvl'] = int(treb.group(1))
        buildings['Требушет']['ppl'] = int(treb.group(2))
        logger.debug("treb: %s" % str(treb.groups()))
        return

    #Нас атаковали
    if re.search(r"Твои владения атакованы!", text):
        war.battle = True
        war.imune = time.time() + 3600 #60 минут (TODO: 30 минут для завоевателя и плохиша)
        timer.setPplTimer(1)
        #Запустить на 1 минуту таймер ремонта стены
        return

    #Мы атаковали
    if re.search(r"Осада началась!", text):
        war.battle = True
        war.cooldown = time.time() + 600 #10 минут (TODO: 5 минут для завоевателя и плохиша)
        timer.setPplTimer(1)
        logger.debug("Сражение началось!")
        return

    #Окончание сражения
    if re.search(r".Битва.+окончена.+", text):
        war.battle = False
        #Обновить время имуна и кд через меню войны
        #Перезапустить апгрейд
        if timer.upgrTimerThread: builder.doUpgrade(timer.upgrTimerBuilding)
        return
