from typing import List

from execution_module.execution_session_module.execution_portfolio_module.combo_session import ComboSession
from global_component_id_generator import GlobalComponentIDGenerator
from session import Session


class StrategySession(Session):

    def __init__(self):
        super().__init__()
        self._id: str = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self.combo_session_list: List[ComboSession] = []
        raise NotImplementedError

    def refresh_status(self):
        for combo_session in self.combo_session_list:
            combo_session.refresh_status()
        raise NotImplementedError
