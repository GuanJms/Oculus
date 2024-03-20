from typing import List, Optional

from abc import abstractmethod
from execution_module.execution_session_module.execution_signal import ExecutionSignal
from session import Session

from weakref import WeakSet


class ExecutionSignalCoordinator(Session):
    def __init__(self):
        super().__init__()
        self._signal_name: Optional[str] = None
        self._signal_list: List[ExecutionSignal] = []
        self._pending_signal_list: WeakSet[ExecutionSignal] = WeakSet()
        self._completed_signal_list: WeakSet[ExecutionSignal] = WeakSet()

    @abstractmethod
    def create_execution_signal(self):
        raise NotImplementedError("Method should be implemented in subclass")

    def refresh_execution_signal_status(self):
        for pending_signal_session in self._pending_signal_list:
            pending_signal_session.refresh_status()
            if pending_signal_session.is_completed():
                self._pending_signal_list.remove(pending_signal_session)
                self._completed_signal_list.add(pending_signal_session)

    def refresh_status(self):
        raise NotImplementedError("TODO: skip for now")
