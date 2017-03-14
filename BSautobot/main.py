from .utils import coroutine

from . import globalobjs
from . import queues
from . import msg_parser
from . import commands

def setSendMsg(cb):
    globalobjs.SendMsg_cb = cb

def setSendInfo(cb):
    globalobjs.SendInfo_cb = cb

@coroutine
def msgRecvd():
    while 1:
        text = (yield)
        msg_parser.msgParser(text)
        queues.queGetNext()

def cmdRecvd(text):
    commands.cmdParser(text)
