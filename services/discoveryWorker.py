import time
import logging
import threading
from constants import *
from services.executorService import ExecutorService
from services.notificationService import NotificationService
from services.deviceRegistryService import DeviceRegistryService


class DiscoveryWorker(threading.Thread):
    _queue = None
    _log = None
    _ns = None
    _deviceRegistryService = None
    _executorService = None

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue
        self._log = logging.getLogger(__name__)
        self._ns = NotificationService.get_instance()
        self._deviceRegistryService = DeviceRegistryService.get_instance()
        self._executorService = ExecutorService.get_instance()

    def run(self):
        while True:
            device_dto = self._queue.get()
            self._discovery_device(device_dto)
            self._queue.task_done()

    def _discovery_device(self, device_dto):
        self._log.debug("Start discovery device %s with ip: %s" % (device_dto.get("name"), device_dto.get("ip")))
        ping_response = self._executorService.exec_ping(device_dto.get("ip"), count=1, timeout=5)

        if not ping_response:
            time.sleep(2)
            ping_response = self._executorService.exec_ping(device_dto.get("ip"), count=3, timeout=15)

        if not ping_response:
            if device_dto.get("status", OFFLINE_STATE) == ONLINE_STATE:
                device_dto["status"] = OFFLINE_STATE
                if device_dto.get("notification", "enable") == "enable":
                    self._ns.notify("%s is offline!" % device_dto.get("name"))
        else:
            device_dto["last_online"] = int(time.time())
            if device_dto.get("status", OFFLINE_STATE) == OFFLINE_STATE:
                device_dto["status"] = ONLINE_STATE
                if device_dto.get("notification", "enable") == "enable":
                    self._ns.notify("%s is online!" % device_dto.get("name"))
        device_dto["last_discovery"] = int(time.time())
        self._deviceRegistryService.update_device(device_dto)
