from . import globalobjs
from . import queues
from . import msg_parser
from . import commands

def setSendMsg(cb):
    globalobjs.SendMsg_cb = cb

def setSendInfo(cb):
    globalobjs.SendInfo_cb = cb

def msgRecvd(text):
    msg_parser.msgParser(text)
    queues.queGetNext()

def cmdRecvd(text):
    commands.cmdParser(text)
