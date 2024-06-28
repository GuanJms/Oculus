from typing import List, Any
from data_system.base_structure.factory.node_factory import NodeFactory
from data_system.base_structure._enums import QuoteType
from data_system.base_structure.nodes.quote_node import QuoteNode


class QuoteNodeFactory(NodeFactory):
    def __init__(
        self,
        timestamp_col: str,
        header: List[str],
    ):
        super().__init__(
            timestamp_col=timestamp_col,
            header=header,
        )

    @staticmethod
    def create_bid_node(quote, timestamp, **kwargs):
        return QuoteNode(
            quote=quote, timestamp=timestamp, quote_type=QuoteType.BID, **kwargs
        )

    @staticmethod
    def create_ask_node(quote, timestamp, **kwargs):
        return QuoteNode(
            quote=quote, timestamp=timestamp, quote_type=QuoteType.BID, **kwargs
        )


