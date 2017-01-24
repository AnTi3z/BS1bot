from . import globalobjs
from .globalobjs import que
from . import msg_parser
from . import commands
import time
import tgl

que_stoped = True

def setSendMsg(cb):
    globalobjs.SendMsg_cb = cb

def setSendInfo(cb):
    globalobjs.SendInfo_cb = cb

def msgRecvd(text):
    global que_stoped

    msg_parser.msgParser(text)
    if not que.empty(): time.sleep(1); globalobjs.SendMsg_cb(que.get_nowait())
    else: que_stoped = True

def cmdRecvd(text):
    global que_stoped

    commands.cmdParser(text)
    if not que.empty() and que_stoped:
        que_stoped = False
        globalobjs.SendMsg_cb("Наверх")
