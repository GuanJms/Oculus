from typing import Optional

from data_system._enums import VolatilityDomain
from data_system.base_structure.nodes._node import Node
from data_system.base_structure._enums import NodeType


class VolNode(Node):
    def __init__(self, value, timestamp, domains, vol_domain):
        super().__init__()
        self.value = value
        self.node_type = NodeType.VOLATILITY
        self.domains = domains
        self.vol_domain = vol_domain
        self.timestamp = timestamp

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def __str__(self):
        return f"VolNode: {self.value} - {self.vol_domain} - {self.timestamp}"
