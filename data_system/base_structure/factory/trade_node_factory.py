from typing import List, Any

from data_system.base_structure.factory.node_factory import NodeFactory
from data_system.base_structure.nodes.trade_node import TradeNode


class TradeNodeFactory(NodeFactory):
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
    def create_trade_node(price, timestamp, **kwargs):
        return TradeNode(price=price, timestamp=timestamp, **kwargs)
