from typing import Optional

from global_component_id_generator import GlobalComponentIDGenerator
from quote_module.quote_module_factory.quote_board_factory import QuoteBoardFactory
from quote_module.quote_module_factory.quote_manager_factory import QuoteManagerFactory


class BacktestDataManager:
    def __init__(self):
        from backtest_module.backtest_manager import BacktestManager
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._backtest_manager: Optional[BacktestManager] = None

    @property
    def id(self):
        return self._id

    @property
    def frequency(self):
        return self.backtest_manager.frequency

    @property
    def ticker_list(self):
        return self.backtest_manager.ticker_list

    @property
    def backtest_manager(self):
        return self._backtest_manager

    @backtest_manager.setter
    def backtest_manager(self, backtest_manager):
        self._backtest_manager = backtest_manager

    def initialize(self):
        """
        Initialize the backtest data manager; this method is called by the initialization manager.
        During initialization process, the backtest should create one QuoteBoardManager and QuoteBard for each ticker.
        """
        quote_board_manager = QuoteManagerFactory.create_quote_manager(frequency_ms=self.frequency)
        for ticker in self.ticker_list:
            quote_board = QuoteBoardFactory
