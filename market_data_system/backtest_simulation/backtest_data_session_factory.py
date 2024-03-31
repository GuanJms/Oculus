from market_data_system.backtest_simulation._backtest_data_session import BacktestDataSession


class BacktestDataSessionFactory:

    @staticmethod
    def create_data_session() -> BacktestDataSession:
        return BacktestDataSession()
