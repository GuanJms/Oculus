from typing import Any, Optional

from time_system.adapters._time_adapter import TimelineAdapter
from time_system._enums import TimelineType
from utils._transmittable_interface import _EventTransmittable
from market_data_system.facade import MarketDataSystemFacade


class MarketDataSystemTimelineAdapter(TimelineAdapter):

    def __init__(self, timeline_id: str, timeline_type: TimelineType):
        super().__init__()
        self._time_id = timeline_id
        self._timeline_type = timeline_type
        self._market_data_system_facade = MarketDataSystemFacade()
        self._market_data_system_facade.connect(connector_id=timeline_id, connector_type=timeline_type)

        raise NotImplementedError

    def send_event(self, receiver: '_EventTransmittable', event: Any, event_data: Any):
        raise NotImplementedError

    def receive_event(self, event: Any, event_data: Any):
        raise NotImplementedError
