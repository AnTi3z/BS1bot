import logging
from .main import msgRecvd
from .main import cmdRecvd
from .main import setSendMsg
from .main import setSendInfo

logging.getLogger(__name__).addHandler(logging.NullHandler())
