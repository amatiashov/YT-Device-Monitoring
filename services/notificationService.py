import logging


class NotificationService(object):
    _instance = None
    _log = None

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls.__init__(cls._instance, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._log = logging.getLogger(__name__)

    def notify(self, msg):
        self._log.info(msg)
