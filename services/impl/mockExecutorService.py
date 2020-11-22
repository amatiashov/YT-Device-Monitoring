import random


class MockExecutorService(object):

    @staticmethod
    def exec_ping(ip_address, count=None, timeout=None):
        return random.choice([True, False])
