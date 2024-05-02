from typing import Optional
from .._enums import NodeType


class Node:
    def __init__(self):
        self.node_type: Optional[NodeType] = None
        self.timestamp: Optional[int] = None

    def get_node_type(self):
        return self.node_type
