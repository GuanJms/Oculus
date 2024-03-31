from typing import List, Dict

from hub.connection._hub_connection import HubConnection


class HubConnectionFactory:
    @staticmethod
    def create_hub_connection(hub_session_ids: List[str], timeline_id: str, data_session_id: str,
                              execution_session_id_dict: Dict[str, str]) -> HubConnection:
        return HubConnection(hub_session_ids=hub_session_ids, timeline_id=timeline_id, data_session_id=data_session_id,
                             execution_session_id_dict=execution_session_id_dict)