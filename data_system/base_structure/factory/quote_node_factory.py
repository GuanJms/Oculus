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
        self._index_map = {col: i for i, col in enumerate(header)} if header else {}

    def create_nodes(self, data: List[List[Any]]):
        raise Exception("Child class must implement this method")

    def set_header(self, header: List[str]):
        self._check_valid_header(header)
        self._header = header
        self._index_map = {col: i for i, col in enumerate(header) if col not in ["", None]}

    @staticmethod
    def create_bid_node(quote, timestamp, **kwargs):
        return QuoteNode(quote=quote, timestamp=timestamp, quote_type=QuoteType.BID, **kwargs)

    @staticmethod
    def create_ask_node(quote, timestamp, **kwargs):
        return QuoteNode(quote=quote, timestamp=timestamp, quote_type=QuoteType.BID, **kwargs)

    def _check_valid_header(self, header: List[str]):
        if not header:
            raise ValueError("Header should not be empty")
        if self._timestamp_col not in header:
            raise ValueError(f"Timestamp column {self._timestamp_col} is missing in the header")
        if len(header) != len(set(header)):
            raise ValueError("Duplicate columns in the header")
