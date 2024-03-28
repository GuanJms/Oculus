from typing import Dict

from _connection import Connection


class ConnectionManager:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConnectionManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._configurations: Dict[Connection] = dict()
        raise NotImplementedError

    def create_connection(self, connector_id, connector_type):
        pass
