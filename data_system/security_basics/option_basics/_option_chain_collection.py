"""
This is class is a AssetCollection of OptionChain objects. It is a subclass of AssetCollection. It is used to store
OptionChain objects.
"""
from typing import Dict

from data_system.security_basics import AssetCollection
from data_system.security_basics.option_basics import OptionChain


class OptionChainCollection(AssetCollection):

    def __init__(self, ticker: str):
        super().__init__()
        self._ticker = ticker
        self._assets: Dict[int, OptionChain] = {}  # key: expiration, value: OptionChain

    def add(self, option_chain: OptionChain):
        expiration = option_chain.expiration
        self._assets[expiration] = option_chain
