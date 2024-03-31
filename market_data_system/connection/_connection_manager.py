from typing import Dict

from _connection import MarketDataSystemConnection


class MarketDataSystemConnectionManager:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MarketDataSystemConnectionManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._configurations: Dict[MarketDataSystemConnection] = {}
        raise NotImplementedError

    def create_connection(self, connector_id, connector_type):
        pass
