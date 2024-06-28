from typing import List, Any

from data_system.base_structure.factory.trade_node_factory import TradeNodeFactory


class StoculusTradeNodeFactory(TradeNodeFactory):
    timestamp_col = "ms_of_day"

    def __init__(self, header: List[str] = None):
        super().__init__(
            header=header,
            timestamp_col=self.timestamp_col,
        )

    def create_nodes(self, data: List[List[Any]], **kwargs):
        date_timestamp = kwargs.get(
            "date_timestamp", 0
        )  # date_timestamp is converted from date to timestamp
        nodes = []
        for row in data:
            timestamp = row[self._index_map[self._timestamp_col]] + date_timestamp
            price = row[self._index_map["price"]]
            size = row[self._index_map["size"]]
            exchange = row[self._index_map["exchange"]]
            condition = row[self._index_map["condition"]]
            trade_node = self.create_trade_node(
                price=price,
                timestamp=timestamp,
                size=size,
                exchange=exchange,
                condition=condition,
            )
            nodes.append(trade_node)
        return nodes

    def create_node_live(self, data: dict, **kwargs):
        option_meta = kwargs.get("option_meta", {})
        date_timestamp = kwargs.get("date_timestamp", 0)
        timestamp = data.get(self.timestamp_col, 0) + date_timestamp
        ms_of_day = data.get(self.timestamp_col, None)
        price = data.get("price", None)
        size = data.get("size", None)
        exchange = data.get("exchange", None)
        condition = data.get("condition", None)

        # option specific data
        strike = option_meta.get("strike", None)
        expiration = option_meta.get("expiration", None)
        right = option_meta.get("right", None)

        trade_node = self.create_trade_node(
            price=price,
            timestamp=timestamp,
            size=size,
            exchange=exchange,
            condition=condition,
            strike=strike,
            expiration=expiration,
            right=right,
            ms_of_day=ms_of_day,
        )
        return trade_node
