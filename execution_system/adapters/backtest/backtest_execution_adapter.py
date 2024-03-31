from typing import Optional, Dict

from execution_system import ExecutionStatusType
from execution_system.adapters import ExecutionSystemHubAdapter
from strategics.repo.core.strategy import StrategyRule
from execution_system.adapters import ExecutionSystemHubConnectionManager
from _enums import OperationMode


class BacktestExecutionHubAdapter(ExecutionSystemHubAdapter):

    def __init__(self):
        self._status = ExecutionStatusType.NONE_INITIATED
        self._operation_mode = OperationMode.BACKTEST

    @property
    def connection_manager(self):
        return ExecutionSystemHubConnectionManager()

    def get_session_id(self, hub_session_id: str) -> str:
        return self.connection_manager.find_execution_session_id(hub_session_id=hub_session_id)

    def get_session_ids(self, hub_session_ids: Optional[list] = None, hub_id: Optional[str] = None) -> Dict[str, str]:
        """
        Get execution session ids dictionary; key: hub_session_id, value: execution_session_id
        """
        if hub_session_ids is not None and hub_id is not None:
            raise ValueError("Either hub_session_ids or hub_id should be provided")
        if hub_session_ids is not None:
            return {hub_session_id: self.connection_manager.find_execution_session_id(hub_session_id=hub_session_id)
                    for hub_session_id in hub_session_ids}
        if hub_id is not None:
            execution_session_ids = self.connection_manager.find_execution_session_id(hub_id=hub_id)
            return {hub_session_id: execution_session_id
                    for hub_session_id, execution_session_id in
                    self.connection_manager.get_hub_session_id_to_execution_session_id().items()
                    if execution_session_id in execution_session_ids}

    def request_sessions(self, hub_id: str, hub_session_ids: list):
        self.connection_manager.create_sessions(hub_id=hub_id, hub_session_ids=hub_session_ids,
                                                operation_mode=self._operation_mode)

    @property
    def status(self):
        return self._status

    def execute(self, strategy_rule_instance: StrategyRule):
        self._status = ExecutionStatusType.PROCESSING

        raise NotImplementedError
