from . import globalobjs
from . import queues

def doBuyReses(wood=0, stone=0, food=0):
    if wood == 0 and stone == 0 and food == 0: return

    queues.queThrdsLock.acquire()
    #Закупаем ресурсы
    queues.msgQueAdd('Наверх')
    queues.msgQueAdd('Торговля')
    queues.msgQueAdd('Купить')

    if wood > 0:
        queues.msgQueAdd('Дерево')
        queues.msgQueAdd(str(wood))
        queues.msgQueAdd('Назад')

    if stone > 0:
        queues.msgQueAdd('Камень')
        queues.msgQueAdd(str(stone))
        queues.msgQueAdd('Назад')

    if food > 0:
        queues.msgQueAdd('Еда')
        queues.msgQueAdd(str(food))
        queues.msgQueAdd('Назад')

    queues.msgQueAdd('Наверх')
    queues.queThrdsLock.release()

    globalobjs.SendInfo_cb('\u2755 Закупка: %d\U0001f332 %d\u26cf %d\U0001f356' % (wood,stone,food))
