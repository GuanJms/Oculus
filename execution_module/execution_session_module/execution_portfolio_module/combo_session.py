from typing import List

from execution_module.execution_session_module.execution_portfolio_module.leg_session import LegSession
from global_component_id_generator import GlobalComponentIDGenerator
from session import Session


class ComboSession(Session):

    def __init__(self):
        super().__init__()
        self._id: str = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._leg_session_list: List[LegSession] = []

    def refresh_status(self):
        raise NotImplementedError
