from typing import Optional, List

from execution_module.execution_session_module.execution_action import ExecutionAction
from session import Session
from weakref import WeakSet


class ExecutionActionCoordinator(Session):

    def __init__(self):
        super().__init__()
        self._class_id: Optional[str] = None
        self._class_name: Optional[str] = None
        self._action_session_list: List[ExecutionAction] = []
        self._pending_action_session_list: WeakSet[ExecutionAction] = WeakSet()
        self._completed_action_session_list: WeakSet[ExecutionAction] = WeakSet()

    def refresh_status(self):
        pass
