from typing import Optional, Dict

from time_system.timeline import TimelineFactory, Timeline
from time_system import TimelineType


class TimelineHubConnectionManager:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TimelineHubConnectionManager, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._timelines: Dict[str, Timeline] = dict()  # key: timeline_id, value: Timeline
        self._hub_id_to_timeline_id: Dict[str, str] = dict()  # key: hub_id, value: timeline_id
        # TODO: Potentially just store into database in the future

    def create_timeline(self, hub_id: str, timeline_type: TimelineType):
        timeline = TimelineFactory.create_timeline(timeline_type=timeline_type)
        self.add_timeline(hub_id=hub_id, timeline_id=timeline.id, timeline=timeline)

    def add_timeline(self, hub_id: str, timeline_id: str, timeline: Timeline):
        self._timelines[timeline_id] = timeline
        self._hub_id_to_timeline_id[hub_id] = timeline_id

    # TODO: Add delete timeline
    def get_timeline_id(self, hub_id) -> Optional[str]:
        return self._hub_id_to_timeline_id.get(hub_id, None)

    def get_timeline(self, timeline_id: Optional[str] = None, hub_id: Optional[str] = None) -> Optional[Timeline]:
        # only one of timeline_id or hub_id should be provided
        if timeline_id is not None and hub_id is not None:
            raise ValueError("Only one of timeline_id or hub_id should be provided")
        if timeline_id is not None:
            return self._timelines.get(timeline_id, None)
        if hub_id is not None:
            timeline_id = self.get_timeline_id(hub_id)
            return self._timelines.get(timeline_id, None)
        return None
