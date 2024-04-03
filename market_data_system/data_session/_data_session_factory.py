from .._enums import OperationMode
from ..backtest_simulation import BacktestDataSessionFactory


class MarketDataSessionFactory:
    @staticmethod
    def create_data_session(operation_mode: OperationMode):
        match operation_mode:
            case OperationMode.BACKTEST:
                BacktestDataSessionFactory.create_data_session()
            case OperationMode.LIVE:
                raise NotImplementedError("Live data session not implemented yet")
            case OperationMode.PAPER:
                raise NotImplementedError("Paper data session not implemented yet")
            case _:
                raise ValueError("Invalid operation mode")
