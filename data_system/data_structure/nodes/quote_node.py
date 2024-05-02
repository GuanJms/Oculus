from data_system.data_structure._enums import NodeType, QuoteType
from data_system.data_structure.nodes.node import Node


class QuoteNode(Node):
    def __init__(self, quote, timestamp, quote_type, **kwargs):
        super().__init__()
        self.quote = quote
        self.timestamp = timestamp
        self.node_type = NodeType.QUOTE
        self.quote_type = quote_type
        self.size = kwargs.get("size", None)
        self.exchange = kwargs.get("exchange", None)
        self.condition = kwargs.get("condition", None)

    def get_quote(self):
        return self._quote

    def __str__(self):
        return f"QuoteNode({self.quote}, {self.timestamp}, {self.quote_type.name}, {self.size}, {self.exchange}, {self.condition})"

    def __repr__(self):
        return self.__str__()
