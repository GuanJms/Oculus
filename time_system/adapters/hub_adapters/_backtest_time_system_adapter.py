from typing import Optional

from time_system.adapters.hub_adapters import TimeSystemHubAdapter, TimelineHubConnectionManager
from time_system.timeline import SimulationTimeline
from time_system import TimelineType


class BacktestTimeSystemHubAdapter(TimeSystemHubAdapter):

    def __init__(self):
        self._timeline: Optional[SimulationTimeline] = None
        self._timeline_type = TimelineType.SIMULATION

    @property
    def connection_manager(self) -> TimelineHubConnectionManager:
        return TimelineHubConnectionManager()

    @property
    def timeline_type(self) -> TimelineType:
        return self._timeline_type

    def get_session_id(self, hub_id: str) -> Optional[str]:
        return self.connection_manager.get_timeline_id(hub_id=hub_id)

    def request_session(self, hub_id: str):
        self.connection_manager.create_timeline(hub_id=hub_id, timeline_type=self._timeline_type)

    def set_timeline_setting(self, **kwargs):
        keys = set(kwargs.keys())
        if start_date := keys.intersection({'start_date'}):
            self._timeline.set_start_date(kwargs[start_date.pop()])
        if end_date := keys.intersection({'end_date'}):
            self._timeline.set_end_date(kwargs[end_date.pop()])
        if start_ms_of_day := keys.intersection({'start_ms_of_day'}):
            self._timeline.set_start_ms_of_day(kwargs[start_ms_of_day.pop()])
        if end_ms_of_day := keys.intersection({'end_ms_of_day'}):
            self._timeline.set_end_ms_of_day(kwargs[end_ms_of_day.pop()])
        if time_interval := keys.intersection({'time_interval'}):
            self._timeline.set_time_interval(kwargs[time_interval.pop()])


