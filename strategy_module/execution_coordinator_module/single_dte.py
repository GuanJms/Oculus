from typing import Optional

from execution_module.execution_session_module.execution_signal_coordinator import \
    ExecutionSignalCoordinator
from execution_module.execution_session_module.execution_signal import ExecutionSignal
from global_component_id_generator import GlobalComponentIDGenerator
from status_module.execution_status_module.signal_session_status_info import SignalStatusInfo
from status_module.execution_status_module.signal_status import SignalStatus


class SingleDTESignal(ExecutionSignal):

    def __init__(self, msd: int, quote_date: int):
        super().__init__()
        self.add_status(status_info=SignalStatusInfo(status=SignalStatus.PENDING, msd=msd, quote_date=quote_date))
        self._signal_name = SingleDTESignal.__name__
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))


class SingleDTESignalCoordinator(ExecutionSignalCoordinator):
    def __init__(self):
        super().__init__()
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._signal_name = SingleDTESignal.__name__

    def create_execution_signal(self):
        signal = SingleDTESignal()
