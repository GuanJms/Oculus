from typing import List, Optional, Type

from backtest_pipeline import BacktestPipeline
from pipeline import PipelineStatusType
from strategics.repo.core.strategy import StrategyRule


def find_idle_pipeline(pipelines: List[BacktestPipeline]) -> Optional[BacktestPipeline]:
    for pipeline in pipelines:
        if pipeline.status == PipelineStatusType.IDLE:
            return pipeline
    return None


class PipelineManager:
    def __init__(self):
        self._strategy_pipeline_dict: dict[Type[StrategyRule], List[BacktestPipeline]] = {}
        self._name_dict: dict[str, Type[StrategyRule]] = {}

    def find_strategy_cls_by_name(self, strategy_name: str) -> Optional[Type[StrategyRule]]:
        return self._name_dict.get(strategy_name, None)

    def get_runnable_pipeline_by_strategy_cls(self, strategy_cls: Type[StrategyRule]) -> Optional[BacktestPipeline]:
        pipelines = self._strategy_pipeline_dict.get(strategy_cls, [])
        if find_idle_pipeline(pipelines) is None:
            new_pipeline = BacktestPipeline()
            new_pipeline.set_strategy_cls(strategy_cls)
            pipelines.append(new_pipeline)
            self._strategy_pipeline_dict[strategy_cls] = pipelines
            return new_pipeline

    def add_strategy(self, strategy_cls: Type[StrategyRule], strategy_name: str):
        if strategy_cls not in self._strategy_pipeline_dict:
            new_pipeline = BacktestPipeline()
            new_pipeline.set_strategy_cls(strategy_cls)
            self._strategy_pipeline_dict[strategy_cls] = [new_pipeline]
        self._name_dict[strategy_name] = strategy_cls

    def run_strategy(self, strategy_cls: Optional[Type[StrategyRule]] = None,
                     strategy_name: Optional[str] = None, **kwargs):
        if strategy_cls is None and strategy_name is None:
            raise ValueError("Either strategy_cls or strategy_name should be provided.")
        if strategy_cls is None:
            strategy_cls = self.find_strategy_cls_by_name(strategy_name)

        runnable_pipeline = self.get_runnable_pipeline_by_strategy_cls(strategy_cls)
        runnable_pipeline.run(**kwargs)

