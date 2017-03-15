import logging
import threading
import queue
import time

from . import globalobjs
from . import builder
from . import tools

logger = logging.getLogger(__name__)

queThrdsLock = threading.Lock()
msgQueue = queue.Queue()
que_stoped = True


def msgQueAdd(msg):
    global que_stoped

    msgQueue.put(msg)
    logger.debug('Add msg: %s', msg)
    if que_stoped:
        que_stoped = False
        queGetNext()

def queGetNext():
    global que_stoped

    if not msgQueue.empty():
        time.sleep(1)
        msg = msgQueue.get()
        globalobjs.SendMsg_cb(msg)
        logger.debug('Send msg: %s', msg)
    else:
        que_stoped = True

def wait():
    while not que_stoped:
        logger.debug('queue wait...')
        time.sleep(1)
