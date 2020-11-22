import os
from queue import Queue
from services.discoveryWorker import DiscoveryWorker
from services.deviceRegistryService import DeviceRegistryService


class DiscoveryService(object):
    _instance = None
    _deviceRegistryService = None
    _discoveryWorkerPool = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.__init__(cls._instance, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._deviceRegistryService = DeviceRegistryService.get_instance()
        self._discoveryWorkerPool = int(os.environ.get("DISCOVERY_WORKER_POOL", 10))

    def discover_devices(self):
        queue = Queue()
        devices = self._deviceRegistryService.get_all_devices()

        for _ in range(len(devices) if len(devices) < self._discoveryWorkerPool else self._discoveryWorkerPool):
            t = DiscoveryWorker(queue)
            t.setDaemon(True)
            t.start()

        for device in devices:
            if device.get("monitoring", "enable") == "enable":
                queue.put(device)

        queue.join()
