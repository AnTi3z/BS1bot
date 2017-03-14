import logging
import threading
import queue
import time

from . import globalobjs
from . import builder
from . import tools

logger = logging.getLogger(__name__)

queThrdsLock = threading.Lock()
cmdQueue = queue.Queue()
msgQueue = queue.Queue()
que_stoped = True


def cmdQueAdd(cmd):
    global que_stoped

    cmdQueue.put(cmd)
    if que_stoped:
        que_stoped = False
        queGetNext()

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
    elif not cmdQueue.empty():
        cmdQueParse()
        queGetNext()
    else:
        que_stoped = True

def cmdQueParse():
    cmd, *params = cmdQueue.get()

    if cmd == 'build':
        builder.doUpgrade(*params)
    elif cmd == 'feed':
        tools.doBuyFood()
    elif cmd == 'reses':
        tools.doTargetReses(*params)
    elif cmd == 'ppl':
        tools.doAutoPpl(*params)

def wait():
    while not que_stoped:
        logger.debug('queue wait...')
        time.sleep(1)
