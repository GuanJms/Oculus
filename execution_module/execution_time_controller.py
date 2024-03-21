from typing import Optional

from global_utils import GlobalComponentIDGenerator, GlobalTimeGenerator


class ExecutionTimeController:

    def __init__(self, time_params: dict[str, int]):
        """
        :param time_params: {'start_date': int, 'end_date': int, 'start_ms_of_day': int,
        'end_ms_of_day': int, 'frequency': int}
        """
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))

        # Static variables
        self._time_params = time_params
        self._start_date: int = time_params.get('start_date')
        self._end_date: int = time_params.get('end_date')
        self._start_ms_of_day: int = time_params.get('start_ms_of_day')
        self._end_ms_of_day: int = time_params.get('end_ms_of_day')
        self._frequency: int = time_params.get('frequency')

        # Dynamic variables
        self._ms_of_day: Optional[int] = None
        self._quote_date: Optional[int] = None

    @property
    def id(self):
        return self._id

    @property
    def ms_of_day(self):
        return self._ms_of_day

    @property
    def quote_date(self):
        return self._quote_date

    @property
    def frequency(self):
        return self._frequency

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def start_ms_of_day(self):
        return self._start_ms_of_day

    @property
    def end_ms_of_day(self):
        return self._end_ms_of_day

    def get_time_params(self):
        return self._time_params

    def initialize(self):
        self._ms_of_day = self.start_ms_of_day
        # check if the start_date is a business day
        if not GlobalTimeGenerator.is_business_day(self.start_date):
            self._quote_date = GlobalTimeGenerator.get_next_business_day(self.start_date)
        else:
            self._quote_date = self.start_date

    def get_execution_status(self) -> str:
        if self._check_end_of_execution():
            return "DONE"
        else:
            return "RUNNING"

    def _check_end_of_execution(self) -> bool:
        if self._quote_date >= self.end_date and self._ms_of_day >= self.end_ms_of_day:
            return True
        else:
            return False

    def get_next_time_message(self):
        if self._need_to_change_quote_date():
            self._set_to_next_business_day()
            MESSAGE = "CHANGE_QUOTE_DATE"
        else:
            MESSAGE = "SAME_QUOTE_DATE"
            self._calculate_next_ms_of_day()
        return self._generate_next_time_message(MESSAGE)

    def _need_to_change_quote_date(self) -> bool:
        return self._ms_of_day >= self.end_ms_of_day

    def _calculate_next_ms_of_day(self):
        if self._ms_of_day + self._frequency >= self.end_ms_of_day:
            self._ms_of_day = self.end_ms_of_day
        else:
            self._ms_of_day += self._frequency

    def _set_to_next_business_day(self):
        self._quote_date = GlobalTimeGenerator.get_next_business_day(self._quote_date)
        self._ms_of_day = self.start_ms_of_day

    def _generate_next_time_message(self, MESSAGE):
        return MESSAGE, self._quote_date, self._ms_of_day


