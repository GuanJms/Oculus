from typing import List, Optional

from asset_module.asset import Asset
from global_component_id_generator import GlobalComponentIDGenerator
from session import Session


class LegSession(Session):

    def __init__(self):
        super().__init__()
        self._id: str = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._asset_type: Optional[str] = None
        self._ticker: Optional[str] = None
        self._asset: Optional[Asset] = None

    def refresh_status(self):
        raise NotImplementedError
