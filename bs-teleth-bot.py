#!/usr/local/bin/python

import threading
import logging
import re
from functools import partial
import telethon.errors
from telethon import TelegramClient
from telethon.tl.types import Updates, UpdateNewMessage, UpdateShortChatMessage, UpdateShortMessage, UpdateEditMessage
from telethon.tl.types import MessageService
from telethon.tl.types import InputPeerChat, InputPeerUser
from telethon.tl.types import PeerChat
# from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.messages import ForwardMessagesRequest
from time import sleep
from config import *


import BSautobot

client = None

logging.basicConfig(level=logging.WARNING,format='[%(asctime)s.%(msecs)d] %(levelname)s:%(name)s:%(funcName)s [lineno %(lineno)d] %(message)s',datefmt='%H:%M:%S')
logging.getLogger("BSautobot").setLevel(logging.DEBUG)


def send_msg_retry(peer, text):
    while True:
        try:
            client.send_message(peer, text)
            break
        except telethon.errors.ServerError:
            sleep(2)
            print('Exception occurred(Server error). Try to resend msg: {}'.format(text))


def init_connection():
    global client
    client = TelegramClient('bs_autobot', API_ID, API_HASH, process_updates=True)
    print('Connecting...')
    if not client.connect():
        print('Connection failed')
    print('Done.')

    if not client.is_user_authorized():
        client.send_code_request(PHONE)
        client.sign_in(PHONE, input('Enter code: '))

    bot_chat = InputPeerUser(BS_BOT_ID, BS_BOT_HASH)
    info_chat = InputPeerChat(CMD_CHAN_ID)
    stat_chat = InputPeerUser(BS_STAT_ID, BS_STAT_HASH)

    # print(client(ResolveUsernameRequest('BastionSiegeBot')))
    # print(client(ResolveUsernameRequest('BSBattleStatsBot')))

    BSautobot.setSendMsg(partial(send_msg_retry, bot_chat))
    BSautobot.setSendInfo(partial(send_msg_retry, info_chat))

    client.send_message(bot_chat,'Наверх')
    sleep(1)
    client.send_message(bot_chat, 'Постройки')
    threading.Timer(2, BSautobot.cmdRecvd, args=['!еда']).start()
    threading.Timer(5, BSautobot.cmdRecvd, args=['!ап']).start()
    threading.Timer(10, BSautobot.cmdRecvd, args=['!люди']).start()


def main_loop():
    while True:
        # sleep(0.1)
        update = client.updates.poll()
        # print(update)
        if isinstance(update, Updates):
            for x in update.updates:
                update_handler(x)
        else:
            update_handler(update)


def update_handler(update):
    # print(update)

    if isinstance(update, UpdateShortChatMessage):
        if update.chat_id == CMD_CHAN_ID and update.message.startswith("!"):
            print('Cmd: {}'.format(update.message))
            BSautobot.cmdRecvd(update.message)
    elif isinstance(update, UpdateShortMessage):
        if update.user_id ==  BS_BOT_ID:
            print('From bot: {}'.format(update.message))
            BSautobot.msgRecvd(update.message)
            if re.search(r"Битва с .+ окончена.+", update.message, re.S) or \
                    re.search(r"Разведчики докладывают.+", update.message, re.S):
                client(ForwardMessagesRequest(InputPeerUser(BS_BOT_ID, BS_BOT_HASH),
                                              (update.id,),
                                              InputPeerUser(BS_STAT_ID, BS_STAT_HASH)))

    elif isinstance(update, UpdateNewMessage):
        if isinstance(update.message, MessageService): return

        if update.message.from_id == BS_BOT_ID:
            print('From bot: {}'.format(update.message.message))
            BSautobot.msgRecvd(update.message.message)
            if re.search(r"Битва с .+ окончена.+", update.message.message, re.S) or \
                    re.search(r"Разведчики докладывают.+", update.message.message, re.S):
                client(ForwardMessagesRequest(InputPeerUser(BS_BOT_ID, BS_BOT_HASH),
                                              (update.message.id,),
                                              InputPeerUser(BS_STAT_ID, BS_STAT_HASH)))
        elif isinstance(update.message.to_id, PeerChat):
            if update.message.to_id.chat_id == CMD_CHAN_ID and update.message.message.startswith("!"):
                print('Cmd: {}'.format(update.message.message))
                BSautobot.cmdRecvd(update.message.message)
    elif isinstance(update, UpdateEditMessage):
        if update.message.from_id == BS_BOT_ID:
            print('From bot: {}'.format(update.message.message))
            BSautobot.msgRecvd(update.message.message)


if __name__ == '__main__':
    init_connection()
    main_loop()
    # client.add_update_handler(update_handler)
    # client.idle()
    client.diconnect()
    # Last command of file (so everything needed is already loaded above)
