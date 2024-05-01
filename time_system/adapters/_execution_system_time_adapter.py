from typing import Any

from time_system.adapters._time_adapter import TimelineAdapter
from time_system._enums import TimelineType
from utils._transmittable_interface import _EventTransmittable


class ExecutionSystemTimelineAdapter(TimelineAdapter):
    def __init__(self, timeline_type: TimelineType):
        super().__init__()
        raise NotImplementedError

    def send_event(self, receiver: "_EventTransmittable", event: Any, event_data: Any):
        pass

    def receive_event(self, event: Any, event_data: Any):
        pass

    def send_timestamp(self):
        pass

    def receive_timestamp(self, time: Any):
        pass
