from status_module.execution_status_module.strategy_section_status import StrategySectionStatus
from status_module.status_info import StatusInfo


class StrategySectionStatusInfo(StatusInfo):
    def __init__(self, status: StrategySectionStatus, **kwargs):
        super().__init__(status, **kwargs)
