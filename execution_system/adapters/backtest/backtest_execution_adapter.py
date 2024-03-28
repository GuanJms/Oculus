from execution_system import ExecutionStatusType
from strategics.repo.core.strategy import StrategyRule


class BacktestExecutionHubAdapter:

    def __init__(self):
        self._status = ExecutionStatusType.NONE_INITIATED


    @property
    def status(self):
        return self._status

    def execute(self, strategy_rule_instance: StrategyRule):
        self._status = ExecutionStatusType.PROCESSING

        raise NotImplementedError
