from typing import List, Optional, Type
from hub._enums import RunningStatusType

from _backtest_hub import BacktestHub
from strategics.repo.core.strategy import StrategyRule


def find_inactive_hub(hubs: List[BacktestHub]) -> Optional[BacktestHub]:
    for hub in hubs:
        if hub.status == RunningStatusType.INACTIVE:
            return hub
    return None


class HubManager:
    def __init__(self):
        self._strategy_hub_dict: dict[Type[StrategyRule], List[BacktestHub]] = {}
        self._name_dict: dict[str, Type[StrategyRule]] = {}

    def find_strategy_cls_by_name(self, strategy_name: str) -> Optional[Type[StrategyRule]]:
        return self._name_dict.get(strategy_name, None)

    def get_runnable_hub_by_strategy_cls(self, strategy_cls: Type[StrategyRule]) -> Optional[BacktestHub]:
        hubs = self._strategy_hub_dict.get(strategy_cls, [])
        if find_inactive_hub(hubs) is None:
            new_hub = BacktestHub()
            new_hub.set_strategy_cls(strategy_cls)
            hubs.append(new_hub)
            self._strategy_hub_dict[strategy_cls] = hubs
            return new_hub

    def add_strategy(self, strategy_cls: Type[StrategyRule], strategy_name: str):
        if strategy_cls not in self._strategy_hub_dict:
            new_hub = BacktestHub()
            new_hub.set_strategy_cls(strategy_cls)
            self._strategy_hub_dict[strategy_cls] = [new_hub]
        self._name_dict[strategy_name] = strategy_cls

    def run_strategy(self, strategy_cls: Optional[Type[StrategyRule]] = None,
                     strategy_name: Optional[str] = None, **kwargs):
        if strategy_cls is None and strategy_name is None:
            raise ValueError("Either strategy_cls or strategy_name should be provided.")
        if strategy_cls is None:
            strategy_cls = self.find_strategy_cls_by_name(strategy_name)

        runnable_hub = self.get_runnable_hub_by_strategy_cls(strategy_cls)
        runnable_hub.run(**kwargs)

