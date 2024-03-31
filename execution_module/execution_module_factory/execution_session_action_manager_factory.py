from execution_module.execution_session_module.action_manager import \
    ExecutionSessionActionManager

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from execution_system.sessions._execution_session import ExecutionSession


class ExecutionSessionActionManagerFactory:

    @classmethod
    def create_execution_session_action_manager(cls,
                                                execute_session: 'ExecutionSession') -> ExecutionSessionActionManager:
        execution_session_action_manager = ExecutionSessionActionManager(execute_session)
        return execution_session_action_manager
