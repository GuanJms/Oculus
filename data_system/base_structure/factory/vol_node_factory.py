from data_system.base_structure.factory.node_factory import NodeFactory
from data_system.base_structure.nodes.vol_node import VolNode


class VolatilityNodeFactory(NodeFactory):
    def __init__(
        self,
        timestamp_col: str,
        header: list,
    ):
        super().__init__(
            timestamp_col=timestamp_col,
            header=header,
        )

    @staticmethod
    def create_volatility_node(value, timestamp, domains, vol_domain):
        return VolNode(value, timestamp, domains, vol_domain)
