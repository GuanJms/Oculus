# singleton lock pattern
import threading


class HubLock:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(HubLock, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        self._lock = threading.Lock()

    def get_lock(self):
        return self._lock
