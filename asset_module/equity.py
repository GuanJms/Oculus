from typing import Optional, List

from global_component_id_generator import GlobalComponentIDGenerator
from asset_module.asset import Asset


class Equity(Asset):

    def __init__(self):
        super().__init__()
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._type = 'equity'
