from backtest_module.backtest_data_session import BacktestDataSession


class BacktestDataSessionFactory:

    @classmethod
    def create_session(cls) -> BacktestDataSession:
        return BacktestDataSession()
