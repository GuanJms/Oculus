from typing import List, Optional

from global_component_id_generator import GlobalComponentIDGenerator
from asset_module.asset import Asset


class Option(Asset):

    def __init__(self):
        super().__init__()
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._ticker: Optional[str] = None
        self._type: str = 'option'
        self._option_type: Optional[str] = None
        self._strike: Optional[int] = None
        self._expiration: Optional[int] = None

    @property
    def option_type(self) -> str:
        return self._option_type

    @property
    def strike(self) -> int:
        return self._strike

    @property
    def expiration(self) -> int:
        return self._expiration
