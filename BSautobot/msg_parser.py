import re
import time

from .globalobjs import *
from . import tools

#парсер сообщений от бота
def msgParser(text):

    res = re.search(r"(?:Жители\s+(\d+).\n)?(?:Армия\s+(\d+).\n)?Золото\s+(\d+).\nДерево\s+(\d+).\nКамень\s+(\d+).\nЕда\s+(\d+).", text)
    if res:
        if res.group(1): buildings['Дома']['ppl'] = int(res.group(1))
        resources['gold'] = int(res.group(3))
        resources['wood'] = int(res.group(4))
        resources['stone'] = int(res.group(5))
        resources['food'] = int(res.group(6))
        resources['time'] = int(time.time()/60)

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

    bld = re.search(r"^.(Лесопилка|Шахта|Ферма|Склад)\s*\n\nУровень\s+(\d+)\nРабочие\s+(\d+)[\s\S]+?\n\n(?:Склад\s+(\d+))?[\s\S]+?Золото\s+(\d+).\nЖители\s+(\d+)[\s\S]+", text)
    if bld:
        build = bld.group(1)

        buildings[build]['lvl'] = int(bld.group(2))
        buildings[build]['ppl'] = int(bld.group(3))
        if bld.group(4): buildings['Склад']['ppl'] = int(bld.group(4))
        resources['gold'] = int(bld.group(5))
        buildings['Дома']['ppl'] = int(bld.group(6))

    wall = re.search(r"^.Стена\s*\n\nУровень\s+(\d+)\nЛучники\s+(\d+)[\s\S]+\nПрочность\s+(\d+).+\n\nЗолото\s+(\d+).\nЖители\s+(\d+)[\s\S]+", text)
    if wall:
        buildings['Стена']['lvl'] = int(wall.group(1))
        buildings['Стена']['ppl'] = int(wall.group(2))
        buildings['Стена']['str'] = int(wall.group(3))
        resources['gold'] = int(wall.group(4))
        buildings['Дома']['ppl'] = int(wall.group(5))

    treb = re.search(r"^.Требушет\s*\n\nУровень\s+(\d+)\nРабочие\s+(\d+)[\s\S]+\n\nЗолото\s+(\d+).\nЖители\s+(\d+)[\s\S]+", text)
    if treb:
        buildings['Требушет']['lvl'] = int(treb.group(1))
        buildings['Требушет']['ppl'] = int(treb.group(2))
        resources['gold'] = int(treb.group(3))
        buildings['Дома']['ppl'] = int(treb.group(4))

    treb = re.search(r"^Мастерская\n\n.Требушет\s+(\d+).+?(\d+).+", text)
    if treb:
        buildings['Требушет']['lvl'] = int(treb.group(1))
        buildings['Требушет']['ppl'] = int(treb.group(2))

    hous = re.search(r"^.Дома\s*\n\nУровень\s+(\d+)\nЖители\s+(\d+)[\s\S]+?Склад\s+(\d+)", text)
    if hous:
        buildings['Дома']['lvl'] = int(hous.group(1))
        buildings['Дома']['ppl'] = int(hous.group(2))
        buildings['Склад']['ppl'] = int(hous.group(3))

    hall = re.search(r"^.Ратуша\s*\n\nУровень\s+(\d+)\nЗолото\s+(\d+)", text)
    if hall:
        buildings['Ратуша']['lvl'] = int(hall.group(1))
        resources['gold'] = int(hall.group(2))

    if re.search(r"Твои владения атакованы!", text) or re.search(r"Осада началась!", text):
        tools.doAutoPpl()
