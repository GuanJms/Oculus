from typing import Union, Optional

from time_system.timeline._timeline import Timeline
from datetime import timedelta, datetime

from time_system.utils._date_time_transformation import check_valid_time_interval, get_milliseconds, get_date
from time_system.adapters import ExecutionSystemTimelineAdapter, MarketDataSystemTimelineAdapter
from time_system._enums import TimeType, TimelineType
from market_data_system._enums import SimulationEventType


class SimulationTimeline(Timeline):

    def __init__(self):
        super().__init__()
        # TimeManager has Time
        self._timeline_type = TimelineType.SIMULATION
        self._time_interval: int = 0  # in milliseconds
        self._start_ms_of_day: int = -1  # in milliseconds
        self._end_ms_of_day: int = -1
        self._start_date: int = -1
        self._end_date: int = -1
        self._execution_system: Optional['ExecutionSystemTimelineAdapter'] = None
        self._market_data_system: Optional['MarketDataSystemTimelineAdapter'] = None
        self.calendar: Calendar = NASDAQCalendar()

    @property
    def time_interval(self):
        return self._time_interval
    #
    # def start(self, **kwargs):
    #     # Start adapter
    #     raise NotImplemented
    #
    #
    #     # Adding market_system and execution_system to event subscribers
    #     self.add_subscriber(self.market_data_system)
    #     self.add_subscriber(self.execution_system)
    #
    #     raise NotImplemented

    # def create_adapters(self): # TODO: what is this?
    #     self._execution_system = ExecutionSystemTimelineAdapter(self.timeline_type)
    #     self._market_data_system = MarketDataSystemTimelineAdapter(self.timeline_type)

    def advance_time(self):
        ms_of_day = self.get_time(TimeType.MS_OF_DAY)

        if ms_of_day < self._start_ms_of_day:
            self.set_time(ms_of_day=self._start_ms_of_day)
            self.publish(SimulationEventType.ADVANCE_MS_OF_DAY, self.get_time(TimeType.MS_OF_DAY))

        if ms_of_day >= self._end_ms_of_day:
            self._advance_date()
        else:
            self._advance_ms_of_day()

    def _advance_ms_of_day(self):
        ms_of_day = self.get_time(TimeType.MS_OF_DAY)
        if ms_of_day + self.time_interval >= self._end_ms_of_day:
            self.set_time(ms_of_day=self._end_ms_of_day)
        else:
            self.set_time(ms_of_day=ms_of_day + self.time_interval)
        self.publish(SimulationEventType.ADVANCE_MS_OF_DAY, self.get_time(TimeType.MS_OF_DAY)

    def _advance_date(self):
        current_date = self.get_time(TimeType.DATE)
        next_date = get_date(self.calendar.get_next_business_day(current_date))
        self.set_time(date=next_date, ms_of_day=self._start_ms_of_day)
        self.publish(SimulationEventType.ADVANCE_DATE, self.get_time(TimeType.DATE))

    # @property
    # def execution_system(self):
    #     return self._execution_system
    #
    # @property
    # def market_data_system(self):
    #     return self._market_data_system

    # def register_execution_system_time_adaptor(self, execution_system_time_adaptor: ExecutionSystemTimelineAdapter):
    #     self._execution_system = execution_system_time_adaptor
    #
    # def register_market_data_system_time_adaptor(self,
    #                                              market_data_system_time_adaptor: MarketDataSystemTimelineAdapter):
    #     self._market_data_system = market_data_system_time_adaptor
    #
    # def unregister_execution_system_time_adaptor(self):
    #     self._execution_system = None
    #
    # def unregister_market_data_system_time_adaptor(self):
    #     self._market_data_system = None

    def set_time_interval(self, time_interval: Union[int, timedelta]):
        check_valid_time_interval(time_interval)
        self._time_interval = get_milliseconds(time_interval)

    def set_start_ms_of_day(self, start_time: Union[int, str, timedelta]):
        self._start_ms_of_day = get_milliseconds(start_time)

    def set_end_ms_of_day(self, end_time: Union[int, str, timedelta]):
        self._end_ms_of_day = get_milliseconds(end_time)

    def set_start_date(self, start_date: Union[int, str, datetime]):
        self._start_date = get_date(start_date)

    def set_end_date(self, end_date: Union[int, str, datetime]):
        self._end_date = get_date(end_date)
