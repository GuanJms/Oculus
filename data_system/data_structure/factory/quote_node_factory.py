from typing import List, Any

from data_system.data_structure._enums import QuoteType
from data_system.data_structure.nodes.quote_node import QuoteNode


class QuoteNodeFactory:
    def __init__(
        self,
        timestamp_col: str,
        header: List[str],
    ):
        self._header = header
        self._timestamp_col = timestamp_col
        self._index_map = {col: i for i, col in enumerate(header)}

    def create_nodes(self, data: List[List[Any]]):
        raise Exception("Child class must implement this method")

    @staticmethod
    def create_bid_node(quote, timestamp, **kwargs):
        return QuoteNode(quote, timestamp, QuoteType.BID, **kwargs)

    @staticmethod
    def create_ask_node(quote, timestamp, **kwargs):
        return QuoteNode(quote, timestamp, QuoteType.ASK, **kwargs)
