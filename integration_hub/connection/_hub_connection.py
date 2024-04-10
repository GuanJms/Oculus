"""
A HubConnection is a class that tracks [HubSession_id]_i ..N, timeline_id, and data_session_id.
"""
from typing import List, Dict, Optional


class HubConnection:

    def __init__(self, hub_session_ids: List[str], timeline_id: str, data_session_id: str,
                 execution_session_id_dict: Dict[str, str]):
        self._hub_session_ids = hub_session_ids
        self._timeline_id: str = timeline_id
        self._data_session_id: str = data_session_id
        self._execution_session_id_dict: Dict[str, str] = execution_session_id_dict
        # key: hub_session_id, value: execution_session_id

    def __str__(self):
        return f"HubConnection({self._hub_session_ids}, {self._timeline_id}, {self._data_session_id})"

    def __repr__(self):
        return f"HubConnection({self._hub_session_ids}, {self._timeline_id}, {self._data_session_id})"

    @property
    def hub_session_ids(self):
        return self._hub_session_ids

    @property
    def timeline_id(self):
        return self._timeline_id

    @property
    def data_session_id(self):
        return self._data_session_id

    def get_execution_session_id(self, hub_session_id: str) -> str:
        return self._execution_session_id_dict.get(hub_session_id, None)


