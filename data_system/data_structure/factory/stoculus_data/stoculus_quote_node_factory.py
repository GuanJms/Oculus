from typing import List, Any

from data_system.data_structure.factory.quote_node_factory import QuoteNodeFactory


class StoculusOptionQuoteNodeFactory(QuoteNodeFactory):
    quote_cols = ["bid", "ask"]
    timestamp_col = "ms_of_day"
    bid_header = ["bid_size", "bid_exchange", "bid_condition"]
    ask_header = ["ask_size", "ask_exchange", "ask_condition"]

    def __init__(self, header: List[str]):
        super().__init__(
            header=header,
            timestamp_col=self.timestamp_col,
        )

    def create_nodes(self, data: List[List[Any]]):
        nodes = []
        for row in data:
            timestamp = row[self._index_map[self._timestamp_col]]
            bid = row[self._index_map['bid']]
            ask = row[self._index_map['ask']]
            bid_size = row[self._index_map['bid_size']]
            bid_exchange = row[self._index_map['bid_exchange']]
            bid_condition = row[self._index_map['bid_condition']]
            ask_size = row[self._index_map['ask_size']]
            ask_exchange = row[self._index_map['ask_exchange']]
            ask_condition = row[self._index_map['ask_condition']]
            bid_node = self.create_bid_node(
                quote=bid,
                timestamp=timestamp,
                size=bid_size,
                exchange=bid_exchange,
                condition=bid_condition,
            )
            ask_node = self.create_ask_node(
                quote=ask,
                timestamp=timestamp,
                size=ask_size,
                exchange=ask_exchange,
                condition=ask_condition,
            )
            nodes.append(bid_node)
            nodes.append(ask_node)
        return nodes