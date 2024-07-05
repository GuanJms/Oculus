from typing import Dict, List

import numpy as np

from data_system._enums import GreekDomain, ModelDomain, DomainEnum
from data_system.base_structure.factory.node_factory import NodeFactory
from data_system.base_structure.nodes import QuoteNode, TradeNode
from data_system.base_structure.nodes.greek_node import GreekNode


class GreekNodeFactory(NodeFactory):
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
    def create_greek_node(
        greek_values: Dict[GreekDomain, float],
        node: TradeNode | QuoteNode,
        timestamp,
        domains: List[DomainEnum],
        model_domain: ModelDomain,
    ):
        return GreekNode(greek_values, node, timestamp, domains, model_domain)
