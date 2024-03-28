"""
A HubConnection is a class that tracks [HubSession_id]_i ..N, timeline_id, and data_session_id.
"""
from typing import List


class HubConnection:

    def __init__(self, hub_session_ids: List[str], timeline_id: str, data_session_id: str):
        self._hub_session_ids = hub_session_ids
        self._timeline_id: str = timeline_id
        self._data_session_id: str = data_session_id

    def __eq__(self, other):
        return (self._hub_session_ids == other._hub_session_ids
                and self._timeline_id == other._timeline_id
                and self._data_session_id == other._data_session_id)

    def __str__(self):
        return f"HubConnection({self._hub_session_ids}, {self._timeline_id}, {self._data_session_id})"

    def __repr__(self):
        return f"HubConnection({self._hub_session_ids}, {self._timeline_id}, {self._data_session_id})"


