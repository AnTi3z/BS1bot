import logging
import threading

from . import globalobjs
from . import queues
from . import msg_parser
from . import commands

logger = logging.getLogger(__name__)

def setSendMsg(cb):
    globalobjs.SendMsg_cb = cb

def setSendInfo(cb):
    globalobjs.SendInfo_cb = cb

def msgRecvd(text):
    # logger.debug('Поток: %s - Сообщение от бота принято',str(threading.current_thread()))
    is_cmd_reply = msg_parser.msgParser(text)
    # logger.debug('Поток: %s - Сообщение обработано парсером',str(threading.current_thread()))
    # logger.debug('Поток: %s - Обработка следующей команды в очереди',str(threading.current_thread()))
    if is_cmd_reply: queues.queGetNext()
    # logger.debug('Поток: %s - Команда в очереди обработана',str(threading.current_thread()))
    

def cmdRecvd(text):
    commands.cmdParser(text)
