import threading
import queue
import time

from . import builder
from . import feeder
from . import globalobjs

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
    cmd_list = cmdQueue.get_nowait()
    cmd = cmd_list[0]
    if len(cmd_list) > 1: params = cmd_list[1:]

    if cmd == 'build':
        if len(cmd_list) > 1: 
            builder.doUpgrade(params[0])
        else:
            builder.doUpgrade()
    elif cmd == 'feed':
        feeder.doBuyFood()
