from market_data_system.backtest_simulation.backtest_data_session import BacktestDataSession


class BacktestDataSessionFactory:

    @classmethod
    def create_session(cls) -> BacktestDataSession:
        return BacktestDataSession()
