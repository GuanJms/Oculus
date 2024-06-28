from typing import Optional
from .._enums import NodeType


class Node:
    def __init__(self):
        self.node_type: Optional[NodeType] = None
        self.timestamp: Optional[int] = None

    def get(self, attr):
        return getattr(self, attr, None)

    def get_node_type(self):
        return self.node_type

    def get_timestamp(self):
        return self.timestamp
