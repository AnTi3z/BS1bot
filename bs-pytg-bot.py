#!/usr/local/bin/python

import logging
from pytg.receiver import Receiver  # get messages
from pytg.sender import Sender  # send messages, and other querys.
from pytg.utils import coroutine
from pytg import Telegram
from functools import partial

import BSautobot

BS_ID = 252148344

logging.basicConfig(level=logging.WARNING,format='[%(asctime)s.%(msecs)d] %(levelname)s:%(name)s:%(funcName)s [lineno %(lineno)d] %(message)s',datefmt='%H:%M:%S')
logging.getLogger("BSautobot").setLevel(logging.DEBUG)

def main():
    #tg = Telegram(telegram="/usr/local/bin/telegram-cli", pubkey_file="/usr/local/etc/telegram-cli/tg-server.pub", port=4458)
    # get a Receiver instance, to get messages.
    receiver = Receiver(host="localhost", port=4458)
    #receiver = tg.receiver

    # get a Sender instance, to send messages, and other querys.
    sender = Sender(host="localhost", port=4458)
    #sender = tg.sender

    # start the Receiver, so we can get messages!
    receiver.start()  # note that the Sender has no need for a start function.

    # add "example_function" function as message listener. You can supply arguments here (like sender).
    receiver.message(main_loop(sender))  # now it will call the example_function and yield the new messages.

    # continues here, after exiting the while loop in example_function()

    # please, no more messages. (we could stop the the cli too, with sender.safe_quit() )
    #sender.terminate()
    #receiver.stop()
    #tg.stop_cli()

    # the sender will disconnect after each send, so there is no need to stop it.
    # if you want to shutdown the telegram cli:
    # sender.safe_quit() # this shuts down the telegram cli.
    # sender.quit() # this shuts down the telegram cli, without waiting for downloads to complete.
    #sender.terminate()
    #receiver.stop()
    #tg.stop_cli()

    print("I am done!")

# this is the function which will process our incoming messages
@coroutine
def main_loop(sender):  # name "example_function" and given parameters are defined in main()
    quit = False
    try:
        while not quit:  # loop for messages
            msg = (yield)  # it waits until the generator has a has message here.
            #sender.status_online()  # so we will stay online.
            # (if we are offline it might not receive the messages instantly,
            #  but eventually we will get them)
            #print(msg)
            if msg.event != "message":
                continue  # is not a message.
            if "text" not in msg or msg.text is None: # we have media instead.
                continue  # and again, because we want to process only text message.
            if msg.own:  # the bot has send this message.
                if msg.text.startswith("!"):
                    #Парсинг команд
                    BSautobot.setSendInfo(partial(sender.send_msg,msg.receiver.cmd))
                    BSautobot.cmdRecvd(msg.text)
                continue
            if msg.sender.peer_id == BS_ID:
                #парсинг сообщений бота
                BSautobot.setSendMsg(partial(sender.send_msg,msg.sender.cmd))
                BSautobot.msgRecvd(msg.text)
                continue
    except GeneratorExit:
        # the generator (pytg) exited (got a KeyboardIterrupt).
        pass
    except KeyboardInterrupt:
        # we got a KeyboardIterrupt(Ctrl+C)
        pass
    else:
        # the loop exited without exception, becaues _quit was set True
        pass

# # program starts here ##
if __name__ == '__main__':
    main()  # executing main function.
    # Last command of file (so everything needed is already loaded above)
