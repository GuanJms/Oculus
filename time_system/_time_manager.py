from typing import Optional, Any, List

from time_system.core import Time
from time_system._enums import TimeType, TimelineType
from utils._transmittable_interface import _EventTransmittable, _EventPublisher, _EventSubscriber
from utils.global_id import GlobalComponentIDGenerator


class TimelineManager(_EventTransmittable, _EventPublisher):

    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self.time = Time(0, 19700101)
        self._event_subscribers: List['_EventSubscriber'] = []
        self._timeline_type: Optional[TimelineType] = None

    @property
    def timeline_type(self):
        return self._timeline_type

    @property
    def id(self):
        return self._id

    def publish(self, event: Any, event_data: Any):
        for subscriber in self._event_subscribers:
            subscriber.receive_event(event, event_data)

    def add_subscriber(self, subscriber: '_EventSubscriber'):
        self._event_subscribers.append(subscriber)

    def delete_subscriber(self, subscriber: '_EventSubscriber'):
        if subscriber in self._event_subscribers:
            self._event_subscribers.remove(subscriber)

    def send_event(self, receiver: '_EventTransmittable', event: Any, event_data: Any):
        receiver.receive_event(event, event_data)

    def receive_event(self, event: Any, event_data: Any):
        pass

    def set_time(self, **kwargs):
        keys = kwargs.keys()
        match True:
            case _ if keys == {'ms_of_day', 'date'}:
                self.time = self.time.set_date_time(ms_of_day=kwargs['ms_of_day'], date=kwargs['date'])
            case _ if keys == {'ms_of_day'}:
                self.time = self.time.set_ms_of_day(kwargs['ms_of_day'])
            case _ if keys == {'date'}:
                self.time = self.time.set_date(kwargs['date'])
            case _ if keys == {'datetime'}:
                self.time = self.time.set_datetime(kwargs['datetime'])
            case _:
                raise ValueError(f"Invalid time setting{keys}")

    def get_time(self, time_type: TimeType):
        self._check_initiated()
        match time_type:
            case TimeType.MS_OF_DAY:
                return self.time.ms_of_day
            case TimeType.DATE:
                return self.time.date
            case TimeType.DATETIME:
                return self.time.to_datetime()
            case _:
                raise ValueError(f"Invalid time type: {time_type}")

    def _check_initiated(self):
        if self.time == Time(0, 1970):
            raise ValueError("Time not set")

    def __eq__(self, other):
        return self.time == other.time

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        return self.time < other.time

    def __le__(self, other):
        return self.time <= other.time

    def __gt__(self, other):
        return self.time > other.time

    def __ge__(self, other):
        return self.time >= other.time
