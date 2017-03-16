import logging
import threading
import queue
import time

from . import globalobjs
from . import builder
from . import tools

logger = logging.getLogger(__name__)

queThrdsLock = threading.RLock()
queStoped = threading.Event()
msgQueue = queue.Queue()


def msgQueAdd(msg):
    msgQueue.put(msg)
    logger.debug('Add msg: %s', msg)
    if queStoped.isSet():
        queStoped.clear()
        logger.debug('queStoped False (Locked)')
        queGetNext()

def queGetNext():
    if not msgQueue.empty():
        logger.debug('Достаем из очереди следующую команду...')
        time.sleep(1)
        msg = msgQueue.get()
        globalobjs.SendMsg_cb(msg)
        logger.debug('Sent msg: %s', msg)
    else:
        queStoped.set()
        logger.debug('queStoped True (Unlocked)')

