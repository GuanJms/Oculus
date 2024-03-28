"""
Each HubSession should only be executing one strategy with one set of parameters.
There could be multiple HubSessions running at the same time with one data sessio.
"""
from typing import Optional, Type, Any

from strategics.repo.core.strategy import StrategyRule
from utils.global_id import GlobalComponentIDGenerator


class HubSession:

    def __init__(self):
        self._id: str = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._strategy_rule_cls: Optional[Type[StrategyRule]] = None
        self._strategy_params: Optional[Any] = None

    @property
    def id(self) -> str:
        return self._id

