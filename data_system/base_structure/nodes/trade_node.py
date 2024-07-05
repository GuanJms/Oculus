from typing import Optional

import numpy as np

from data_system.base_structure._enums import NodeType
from data_system.base_structure.nodes._node import Node
from data_system.utils.time_operations import convert_timestamp_to_datetime


class TradeNode(Node):
    def __init__(self, price, timestamp, **kwargs):
        super().__init__()
        self.price = price
        self.timestamp: int = timestamp
        self.datetime: np.datetime64 = convert_timestamp_to_datetime(
            timestamp
        )  # timestamp is in ms
        self.node_type = NodeType.TRADE
        self.size = kwargs.get("size", None)
        self.log_size_scaled = np.log(self.size) * 2 if self.size is not None else None
        self.exchange = kwargs.get("exchange", None)
        self.condition = kwargs.get("condition", None)
        self.ms_of_day = kwargs.get("ms_of_day", None)

        # if self.price is None or self.timestamp is None or self.datetime is None:
        #     raise ValueError("price, timestamp, and datetime cannot be None")

        # option specific fields
        self.iv = kwargs.get("iv", None)
        self.delta = kwargs.get("delta", None)
        self.gamma = kwargs.get("gamma", None)
        self.theta = kwargs.get("theta", None)
        self.vega = kwargs.get("vega", None)
        self.rho = kwargs.get("rho", None)
        self.vomma = kwargs.get("vomma", None)

    def get_price(self):
        return self.price

    def set_iv(self, iv):
        self.iv = iv

    def set_delta(self, delta):
        self.delta = delta

    def set_gamma(self, gamma):
        self.gamma = gamma

    def set_theta(self, theta):
        self.theta = theta

    def set_vega(self, vega):
        self.vega = vega

    def set_rho(self, rho):
        self.rho = rho

    def set_vomma(self, vomma):
        self.vomma = vomma

    def __str__(self):
        return (
            f"TradeNode(P: {round(self.price, 2)}, "
            f"timestamp: {self.timestamp}, "
            f"size: {self.size}, "
            f"Exg:{self.exchange}, "
            f"Cond:{self.condition}, "
            f"IV: {self.iv},"
            f"Delta: {round(self.delta, 2) if self.delta else None}, "
            f"Gamma: {round(self.gamma, 2) if self.gamma else None}, "
            f"Theta: {round(self.theta, 2) if self.theta else None},"
            f"Vega: {round(self.vega, 2) if self.vega else None},"
            f"Rho: {round(self.rho, 2) if self.rho else None},"
            f"Vomma: {round(self.vomma, 2) if self.vomma else None}"
        )

    def __repr__(self):
        return self.__str__()
