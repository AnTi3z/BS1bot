from .globals import *
import re
import time

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
    if bld.group(1): buildings['storage']['lvl'] = bld.group(1); buildings['storage']['ppl'] = bld.group(2)
    if bld.group(3): buildings['houses']['lvl'] = bld.group(3); buildings['houses']['ppl'] = bld.group(4)
    if bld.group(5): buildings['farm']['lvl'] = bld.group(5); buildings['farm']['ppl'] = bld.group(6)
    if bld.group(7): buildings['sawmill']['lvl'] = bld.group(7); buildings['sawmill']['ppl'] = bld.group(8)
    if bld.group(9): buildings['mine']['lvl'] = bld.group(9); buildings['mine']['ppl'] = bld.group(10)

    if bld.group(11): war_bldngs['barracks']['lvl'] = bld.group(11); war_bldngs['barracks']['ppl'] = bld.group(12)
    if bld.group(13): war_bldngs['wall']['lvl'] = bld.group(13); war_bldngs['wall']['lvl'] = bld.group(14)
