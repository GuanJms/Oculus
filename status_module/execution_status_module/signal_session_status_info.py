from status_module.execution_status_module.signal_status import SignalStatus
from status_module.status_info import StatusInfo


class SignalStatusInfo(StatusInfo):
    def __init__(self, status: SignalStatus, **kwargs):
        super().__init__(status, **kwargs)
