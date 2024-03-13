from backtest_module.backtest_data_section import BacktestDataSection


class BacktestDataSectionFactory:

    @classmethod
    def create_section(cls) -> BacktestDataSection:
        return BacktestDataSection()
