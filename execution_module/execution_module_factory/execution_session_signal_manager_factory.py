from execution_module.execution_session_module.signal_manager import \
    ExecutionSessionSignalManager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from execution_module.execution_session_module.execution_session import ExecutionSession


class ExecutionSessionSignalManagerFactory:
    @classmethod
    def create_execution_session_signal_manager(cls, execution_session: 'ExecutionSession'):
        execution_session_signal_manager = ExecutionSessionSignalManager(execution_session)
        return execution_session_signal_manager
