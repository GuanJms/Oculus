from ._backtest_data_session import BacktestDataSession

class BacktestDataSessionFactory:

    @staticmethod
    def create_data_session() -> BacktestDataSession:
        return BacktestDataSession()
