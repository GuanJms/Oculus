from datetime import datetime, timedelta
from functools import wraps


class FrequencyLimiter:
    update_frequency_ms = 100

    def __init__(self):
        self.last_update_timestamps = {}

    def is_limited(self, __name__, timestamp=None):
        if __name__ not in self.last_update_timestamps:
            self.last_update_timestamps[__name__] = None
            return False
        else:
            if timestamp is None:
                timestamp = datetime.now().timestamp() * 1000
            return (
                timestamp - self.last_update_timestamps[__name__]
                < self.update_frequency_ms
            )

    def update(self, __name__, timestamp=None):
        if timestamp is None:
            timestamp = datetime.now().timestamp() * 1000
        self.last_update_timestamps[__name__] = timestamp

    @classmethod
    def set_update_frequency(cls, update_frequency_ms):
        cls.update_frequency_ms = update_frequency_ms
