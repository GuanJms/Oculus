"""
Configuration manager should manager the configuration of the hub system, that include the intergration.
"""
from typing import Dict

from hub.connection._hub_connection import HubConnection


class HubConnectionManager:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(HubConnectionManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.hub_connections: Dict[str, HubConnection] = dict()  # key: hub_id, value: HubConnection

    def add_hub_connection(self, hub_id: str, hub_connection: HubConnection):
        if hub_id in self.hub_connections:
            raise ValueError(f"Hub connection with hub_id {hub_id} already exists; Use update_hub_connection instead.")
        self.hub_connections[hub_id] = hub_connection

    def update_hub_connection(self, hub_id: str, hub_connection: HubConnection):
        if hub_id not in self.hub_connections:
            raise ValueError(f"Hub connection with hub_id {hub_id} does not exist; Use add_hub_connection instead.")
        self.hub_connections[hub_id] = hub_connection

    def get_hub_connection(self, hub_id: str) -> HubConnection:
        return self.hub_connections.get(hub_id, None)

