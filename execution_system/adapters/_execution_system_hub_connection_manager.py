from typing import Dict, List, Optional
from _enums import OperationMode
from execution_system.sessions import ExecutionSessionFactory, ExecutionSession


class ExecutionSystemHubConnectionManager:
    instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ExecutionSystemHubConnectionManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._execution_sessions: Dict[
            str, ExecutionSession] = dict()  # key: execution_session_id, value: ExecutionSession
        self._hub_session_id_to_execution_session_id: Dict[
            str, str] = dict()  # key: hub_session_id, value: execution_session_id
        self._hub_id_to_execution_session_ids: Dict[
            str, list] = dict()  # key: hub_id, value: list of execution_session_ids

    def create_sessions(self, hub_id: str, hub_session_ids: List[str], operation_mode: OperationMode):
        for hub_session_id in hub_session_ids:
            self._create_execution_session(hub_session_id=hub_session_id, operation_mode=operation_mode)

        for hub_session_id in hub_session_ids:
            execution_session_id = self.find_execution_session_id(hub_session_id=hub_session_id)
            if execution_session_id is None:
                raise ValueError(f"Creation of execution session failed {hub_session_id}")
            self._hub_id_to_execution_session_ids[hub_id].append(execution_session_id)

    def find_execution_session(self, hub_id: Optional[str] = None,
                               hub_session_id: Optional[str] = None,
                               execution_session_id: Optional[str] = None, ) -> None | list[
        ExecutionSession] | ExecutionSession:
        if len([x for x in [hub_session_id, execution_session_id, hub_id] if x is not None]) != 1:
            raise ValueError(
                "Find execution session requires exactly one of hub_session_id, execution_session_id, hub_id to be provided")
        if hub_id is not None:
            execution_session_ids = self._hub_id_to_execution_session_ids.get(hub_id, None)
            if execution_session_ids is None:
                return None
            execution_sessions_to_return = []
            for execution_session_id in execution_session_ids:
                execution_session = self._execution_sessions.get(execution_session_id, None)
                if execution_session is not None:
                    execution_sessions_to_return.append(execution_session)
            return execution_sessions_to_return

        if hub_session_id is not None:
            execution_session_id = self._hub_session_id_to_execution_session_id.get(hub_session_id, None)
            return self.find_execution_session(execution_session_id=execution_session_id)
        if execution_session_id is not None:
            return self._execution_sessions.get(execution_session_id, None)
        return None

    def find_execution_session_id(self, hub_id: Optional[str] = None,
                                  hub_session_id: Optional[str] = None) -> None | str | list[str]:
        """
        hub_id -> dict of hub_session_id: execution_session_id
        hub_session_id -> execution_session_id
        """
        if all([x is None for x in [hub_id, hub_session_id]]):
            return None
        if len([x for x in [hub_session_id, hub_id] if x is not None]) != 1:
            raise ValueError(
                "Find execution session requires exactly one of hub_session_id, execution_session_id, hub_id to be provided")
        if hub_id is not None:
            execution_session_ids = self._hub_id_to_execution_session_ids.get(hub_id, None)
            return execution_session_ids
        if hub_session_id is not None:
            return self._hub_session_id_to_execution_session_id.get(hub_session_id, None)

    def get_hub_session_id_to_execution_session_id(self) -> Dict[str, str]:
        return self._hub_session_id_to_execution_session_id

    def find_hub_session_id(self, execution_session_id: str) -> Optional[str]:
        for hub_session_id, _execution_session_id in self._hub_session_id_to_execution_session_id.items():
            if _execution_session_id == execution_session_id:
                return hub_session_id
        return None

    def _create_execution_session(self, hub_session_id: str, operation_mode: OperationMode):
        execution_session = ExecutionSessionFactory.create_session(operation_mode=operation_mode)
        self.add_execution_session(execution_session)
        self._hub_session_id_to_execution_session_id[hub_session_id] = execution_session.id

    def add_execution_session(self, execution_session: ExecutionSession):
        self._execution_sessions[execution_session.id] = execution_session
