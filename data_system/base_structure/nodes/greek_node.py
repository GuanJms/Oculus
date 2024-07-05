from typing import Dict, List

import numpy as np

from data_system._enums import GreekDomain, ModelDomain, DomainEnum
from data_system.base_structure.nodes import QuoteNode, TradeNode
from data_system.base_structure.nodes._node import Node
from data_system.base_structure._enums import NodeType


class GreekNode(Node):
    def __init__(
        self,
        greek_values: Dict[GreekDomain, float | np.float32 | np.float64],
        node: TradeNode | QuoteNode,
        timestamp: int,
        domains: List[DomainEnum],
        model_domain: ModelDomain,
    ):
        super().__init__()
        self.underlying_node = node
        self.node_type = NodeType.GREEK
        self.model_domain = model_domain
        self.timestamp = timestamp
        self.datetime: np.datetime64 = self.underlying_node.datetime
        self.size = self.underlying_node.size
        self.log_size_scaled = self.underlying_node.log_size_scaled
        self.domains = domains

        self.delta = greek_values.get(GreekDomain.DELTA, None)
        self.gamma = greek_values.get(GreekDomain.GAMMA, None)
        self.theta = greek_values.get(GreekDomain.THETA, None)
        self.vega = greek_values.get(GreekDomain.VEGA, None)
        self.rho = greek_values.get(GreekDomain.RHO, None)
        self.vomma = greek_values.get(GreekDomain.VOMMA, None)

    def __str__(self):
        return f"GreekNode - Delta: {self.delta}, Gamma: {self.gamma}, Theta: {self.theta}, Vega: {self.vega}, Rho: {self.rho}, Vomma: {self.vomma}"

    def __repr__(self):
        return self.__str__()
