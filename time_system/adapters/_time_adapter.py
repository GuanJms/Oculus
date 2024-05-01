from typing import Any, Optional

from utils._transmittable_interface import (
    _TimeStampedTransmittable,
    _EventTransmittable,
    _EventSubscriber,
)


class TimelineAdapter(_TimeStampedTransmittable, _EventTransmittable, _EventSubscriber):
    def __init__(self):
        self._system: Optional["_EventSubscriber"] = None

    @property
    def system(self):
        return self._system

    def send_timestamp(self):
        pass

    def receive_timestamp(self, time: Any):
        pass

    def receive_event(self, event: Any, event_data: Any):
        self.system.event_subscriber.receive()

    def send_event(self, receiver: "_EventTransmittable", event: Any, event_data: Any):
        pass

    # def register_target_system_adapter(self, target_system_adapter: _TimeStampedCommunication):
    #     self._system = target_system_adapter
    #
    # def unregister_target_system_adapter(self):
    #     self._system = None
    #
    # def register_time_manager(self, time_manager: TimelineManager):
    #     self._time_manager = time_manager
    #
    # def unregister_time_manager(self):
    #     self._time_manager = None
    #
    # def runnable(self) -> bool:
    #     return self.target_system_adapter is not None and self.time_manager is not None
    #
    # @property
    # def time_manager(self) -> Optional[TimelineManager]:
    #     return self._time_manager
    #
    # def set_time_manager(self, time_manager):
    #     self._time_manager = time_manager
    #
    # def send_timestamp(self):
    #     timestamp = self.time_manager.get_time(TimeType.DATETIME)
    #     self.target_system_adapter.receive_timestamp(timestamp)
    #
    # def receive_timestamp(self, time: Any):
    #     time = get_datetime(time)
    #     self.time_manager.set_time(datetime=time)
