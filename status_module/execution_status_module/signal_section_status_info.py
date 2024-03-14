from status_module.execution_status_module.signal_section_status import SignalSectionStatus
from status_module.status_info import StatusInfo


class SignalSectionStatusInfo(StatusInfo):
    def __init__(self, status: SignalSectionStatus, **kwargs):
        super().__init__(status, **kwargs)
