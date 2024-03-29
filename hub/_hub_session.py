"""
Each HubSession should only be executing one strategy with one set of parameters.
There could be multiple HubSessions running at the same time with one data sessio.
"""
from typing import Optional, Type, Any

from hub._enums import HubType
from strategics.repo.core.strategy import StrategyRule
from utils.global_id import GlobalComponentIDGenerator
from utils.attribute import check_attribute_exist

class HubSession:

    def __init__(self, *args, **kwargs):
        check_attribute_exist(attributes=['hub_type', 'strategy_params', 'strategy_rule_cls'], args=kwargs)
        self._id: str = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._strategy_rule_cls: Optional[Type[StrategyRule]] = kwargs.get()
        self._strategy_params: Optional[Any] = None
        self._hub_type = hub_type

    @property
    def id(self) -> str:
        return self._id

