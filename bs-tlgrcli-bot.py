import tgl
import pprint
import time
from functools import partial
import BSautobot

our_id = 0
pp = pprint.PrettyPrinter(indent=4)

binlog_done = False;

def on_binlog_replay_end():
    global binlog_done
    binlog_done = True;


def on_get_difference_end():
    pass

def on_our_id(id):
    global our_id
    our_id = id
    return "Set ID: " + str(our_id)

def msg_cb(success, msg):
    pp.pprint(success)
    pp.pprint(msg)

HISTORY_QUERY_SIZE = 100

def history_cb(msg_list, peer, success, msgs):
  print(len(msgs))
  msg_list.extend(msgs)
  print(len(msg_list))
  if len(msgs) == HISTORY_QUERY_SIZE:
    tgl.get_history(peer, len(msg_list), HISTORY_QUERY_SIZE, partial(history_cb, msg_list, peer));


def cb(success):
    print(success)

def on_msg_receive(msg):
    if not binlog_done:
      return

    if msg.out: # комманды отправляемые в чат
      #парсинг пользовательских команд
        if msg.text.startswith("!"):
            BSautobot.setSendInfo(msg.dest.send_msg)
            BSautobot.cmdRecvd(msg.text)

    elif msg.dest.id == our_id: # сообщение нам
      if msg.src.id == 252148344: # сообщение от Bastion Siege
        BSautobot.setSendMsg(tgl.Peer(type=tgl.PEER_USER,id=252148344).send_msg)
        BSautobot.msgRecvd(msg.text)

    else: # chatroom
      peer = msg.dest


def on_secret_chat_update(peer, types):
    return "on_secret_chat_update"

def on_user_update(peer, what_changed):
    pass

def on_chat_update(peer, what_changed):
    pass

def on_loop():
    pass

# Set callbacks
tgl.set_on_binlog_replay_end(on_binlog_replay_end)
tgl.set_on_get_difference_end(on_get_difference_end)
tgl.set_on_our_id(on_our_id)
tgl.set_on_msg_receive(on_msg_receive)
tgl.set_on_secret_chat_update(on_secret_chat_update)
tgl.set_on_user_update(on_user_update)
tgl.set_on_chat_update(on_chat_update)
tgl.set_on_loop(on_loop)
