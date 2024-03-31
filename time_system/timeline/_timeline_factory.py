from time_system import SimulationTimeline
from time_system._enums import TimelineType
from time_system.timeline import Timeline


class TimelineFactory:
    @staticmethod
    def create_timeline(timeline_type: TimelineType) -> Timeline:
        match timeline_type:
            case TimelineType.SIMULATION:
                return SimulationTimeline()
            case TimelineType.REALTIME:
                raise NotImplementedError
            case _:
                raise ValueError(f"Invalid timeline type {timeline_type}")