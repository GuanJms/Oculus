from typing import Optional

from data_system.base_structure._enums import NodeType, QuoteType
from data_system.base_structure.nodes._node import Node


class QuoteNode(Node):
    def __init__(self, quote, timestamp, quote_type, **kwargs):
        super().__init__()
        print(f"QuoteNode: {quote}, {timestamp}, {quote_type}, {kwargs}")
        self.quote = quote
        self.timestamp = timestamp
        self.node_type = NodeType.QUOTE
        self.quote_type = quote_type
        self.size = kwargs.get("size", None)
        self.exchange = kwargs.get("exchange", None)
        self.condition = kwargs.get("condition", None)

        # contract specific fields are not in the node since they are not common to all trade nodes
        self.iv = kwargs.get("iv", None)

    def get_quote(self):
        return self.quote

    def set_iv(self, iv):
        self.iv = iv

    def __str__(self):
        return f"QuoteNode(P: {self.quote}, T: {self.timestamp}, B/A:{self.quote_type.name}, V: {self.size}, Exg:{self.exchange}, Cond:{self.condition}"

    def __repr__(self):
        return self.__str__()
