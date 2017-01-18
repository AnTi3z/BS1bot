from .globals import que
from . import msg_parser
from . import commands
import time
import tgl

que_stoped = True

def setBSpeer(peer):
    global BSpeer
    BSpeer = peer

def msgRecvd(text):
    global que_stoped, BSpeer

    msg_parser.msgParser(text)
    if not que.empty(): time.sleep(1); BSpeer.send_msg(que.get_nowait())
    else: que_stoped = True

def msgSent(text):
    global que_stoped, BSpeer

    commands.cmdParser(text)
    if not que.empty() and que_stoped:
        que_stoped = False
        BSpeer.send_msg("Наверх")
