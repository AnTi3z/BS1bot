from .globals import que
from . import msg_parser
from . import commands
import time
import tgl

que_stoped = True

def setSendMsg(cb):
    global SendMsg_cb
    SendMsg_cb = cb

def msgRecvd(text):
    global que_stoped, BSpeer

    msg_parser.msgParser(text)
    if not que.empty(): time.sleep(1); SendMsg_cb(que.get_nowait())
    else: que_stoped = True

def cmdSent(text):
    global que_stoped, BSpeer

    commands.cmdParser(text)
    if not que.empty() and que_stoped:
        que_stoped = False
        SendMsg_cb("Наверх")
