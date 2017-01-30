import time
import threading
from . import builder

upgrTimerThread = None

def setUpgrTimer(bld, minutes):
    global upgrTimerThread
    global upgrTimerStoptime

    if upgrTimerThread: upgrTimerThread.cancel()
    upgrTimerThread = threading.Timer(minutes*60, builder.doUpgrade, args=[bld])
    upgrTimerThread.daemon = True
    upgrTimerThread.start()
    upgrTimerStoptime = time.time() + minutes*60

