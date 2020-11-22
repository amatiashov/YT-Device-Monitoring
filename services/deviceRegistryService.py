import os
import sys
import json
import logging

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")


class DeviceRegistryService(object):
    _instance = None
    _dev_dir = None
    _log = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.__init__(cls._instance, *args, **kwargs)
        return cls._instance

    def _make_folders(self):
        if not os.path.exists(self._dev_dir):
            os.makedirs(self._dev_dir)

    def __init__(self):
        self._log = logging.getLogger(__name__)
        self._dev_dir = os.path.join(RESOURCES_DIR, "devices")
        # self._make_folders()

    def get_all_devices(self):
        devices = []
        for dev in [dev for dev in os.listdir(self._dev_dir) if dev.endswith(".json")]:
            try:
                with open(os.path.join(self._dev_dir, dev)) as device:
                    devices.append(json.loads(device.read()))
            except Exception as e:
                self._log.error("Cannot read device %s: %s" % (dev, str(e)))
        return sorted(devices, key=lambda entity: entity.get("index", sys.maxsize))

    def update_device(self, device):
        with open(os.path.join(self._dev_dir, device.get("name") + ".json"), "w") as f:
            return f.write(json.dumps(device, indent=4))
