"""
Each HubSession should only be executing one strategy with one set of parameters.
There could be multiple HubSessions running at the same time with one data sessio.
"""
from typing import Optional, Type, Any

from integration_hub._enums import HubType
from strategics.repo.core.strategy import StrategyRule
from utils.global_id import GlobalComponentIDGenerator



class HubSession:

    def __init__(self, *args, **kwargs):
        self._id: str = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._strategy_rule_cls: Type[StrategyRule] = kwargs.get('strategy_rule_cls')
        self._strategy_params: Optional[Any] = kwargs.get('strategy_params')
        self._hub_type: HubType = kwargs.get('hub_type')

    @property
    def id(self) -> str:
        return self._id
