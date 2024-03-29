"""
This class is factory that builds hub sessions.
"""
from typing import Optional, Any, Type

from hub._enums import HubType
from hub._hub_session import HubSession
from utils.attribute import check_attribute_exist
from strategics.repo.core.strategy import StrategyRule



class HubSessionFactory:

    @classmethod
    def create(cls, hub_type: HubType, strategy_rule_cls: Type[StrategyRule] = None, strategy_params: Optional[Any] = None, *args, **kwargs) -> HubSession:
        match cls:
            case HubType.BACKTESTING:
                args = {'hub_type': hub_type, 'strategy_params': strategy_params, 'strategy_rule_cls': strategy_rule_cls}
                check_attribute_exist(attributes=['hub_type', 'strategy_params', 'strategy_rule_cls'], args=args)
                hub_session = HubSession(hub_type=cls, strategy_params=kwargs['strategy_params'],
                                         strategy_rule_cls=kwargs['strategy_rule_cls'])
                return hub_session
            case HubType.LIVE_TRADING:
                raise NotImplementedError("Live trading is not implemented yet")
            case HubType.PAPER_TRADING:
                raise NotImplementedError("Paper trading is not implemented yet")
            case _:
                raise Exception(f"Invalid hub type: {cls}")
