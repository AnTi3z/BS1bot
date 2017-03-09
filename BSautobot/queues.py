import threading
import queue
import time

from . import globalobjs
from . import builder
from . import tools

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
    if que_stoped:
        que_stoped = False
        queGetNext()

def queGetNext():
    global que_stoped

    if not msgQueue.empty():
        time.sleep(1)
        globalobjs.SendMsg_cb(msgQueue.get_nowait())
    elif not cmdQueue.empty():
        cmdQueParse()
        queGetNext()
    else:
        que_stoped = True

def cmdQueParse():
    cmd, *params = cmdQueue.get_nowait()

    if cmd == 'build':
        builder.doUpgrade(*params)
    elif cmd == 'feed':
        tools.doBuyFood()
    elif cmd == 'reses':
        tools.doTargetReses(*params)
    elif cmd == 'ppl':
        tools.doAutoPpl(*params)
