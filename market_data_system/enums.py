from enum import Enum


class OperationMode(Enum):
    LIVE_TRADING = "LIVE_TRADING"
    BACKTESTING = "BACKTESTING"
    PAPER_TRADING = "PAPER_TRADING"


