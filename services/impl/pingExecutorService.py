import os
import logging


class PingExecutorService(object):
    _log = None

    def __init__(self):
        self._log = logging.getLogger(__name__)

    def exec_ping(self, ip_address, count=1, timeout=5):
        response = os.system("ping -c %d -W %d %s" % (count, timeout, ip_address))
        self._log.debug("Device %s. Response %s" % (ip_address, str(response)))
        return response == 0
