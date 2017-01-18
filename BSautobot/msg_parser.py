from .globals import *
import re
import time

#парсер сообщений от бота
def msgParser(text):
    res = re.search(r"(?:Жители\s+(\d+).\n)?(?:Армия\s+(\d+).\n)?Золото\s+(\d+).\nДерево\s+(\d+).\nКамень\s+(\d+).\nЕда\s+(\d+).", text)
    if res:
        resources['gold'] = int(res.group(3))
        resources['wood'] = int(res.group(4))
        resources['stone'] = int(res.group(5))
        resources['food'] = int(res.group(6))
        resources['time'] = int(time.time()/60)

    bld = re.search(r"^Постройки\n\n(?:\U0001f3e4\s+(\d+).+\n)?(?:\U0001f3da\s+(\d+).+\s+(\d+)/.+\n)?(?:\U0001f3d8\s+(\d+).+\s+(\d+)/.+\n)?(?:\U0001f33b\s+(\d+).+\s+(\d+)/.+\n)?(?:\U0001f332\s+(\d+).+\s+(\d+)/.+\n)?(?:\u26cf\s+(\d+).+\s+(\d+)/.+\n)?(?:\U0001f6e1\s+(\d+).+\s+(\d+)/.+\n)?(?:\U0001f3f0\s+(\d+).+\s+(\d+)/.+\n)?\nЧто будем строить\?$", text)
    if bld:
      if bld.group(1): buildings['hall']['lvl'] = int(bld.group(1))
      if bld.group(2): buildings['storage']['lvl'] = int(bld.group(2)); buildings['storage']['ppl'] = int(bld.group(3))
      if bld.group(4): buildings['houses']['lvl'] = int(bld.group(4)); buildings['houses']['ppl'] = int(bld.group(5))
      if bld.group(6): buildings['farm']['lvl'] = int(bld.group(6)); buildings['farm']['ppl'] = int(bld.group(7))
      if bld.group(8): buildings['sawmill']['lvl'] = int(bld.group(8)); buildings['sawmill']['ppl'] = int(bld.group(9))
      if bld.group(10): buildings['mine']['lvl'] = int(bld.group(10)); buildings['mine']['ppl'] = int(bld.group(11))

      if bld.group(12): war_bldngs['barracks']['lvl'] = int(bld.group(12)); war_bldngs['barracks']['ppl'] = int(bld.group(13))
      if bld.group(14): war_bldngs['wall']['lvl'] = int(bld.group(14)); war_bldngs['wall']['lvl'] = int(bld.group(15))