from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from execution_system.sessions._execution_session import ExecutionSession


class ExecutionSessionActionManager:

    def __init__(self, execute_session: 'ExecutionSession'):
        self._execute_session = execute_session

    raise NotImplementedError("TODO: implement ExecutionSessionActionManager")
