from status_module.execution_status_module.strategy_session_status import StrategySessionStatus
from status_module.status_info import StatusInfo


class StrategySessionStatusInfo(StatusInfo):
    def __init__(self, status: StrategySessionStatus, **kwargs):
        super().__init__(status, **kwargs)
