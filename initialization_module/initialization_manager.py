"""
InitializationManager is used to initialize the backtest module, execution module: BacktestManager, ExecutionManager,
BacktestDataManager.
"""
from typing import Optional

from configuration_module.configuration_manager import ConfigurationManager
from data_process_module.traded_quote_data_manager import TradedQuoteDataManager


class InitializationManager:
    _data_manager: Optional[TradedQuoteDataManager] = None
    _backtest_manager_list = []
    _initialized = False

    @classmethod
    def get_traded_quote_data_manager(cls):
        cls._initialized_checker()
        return cls._data_manager

    @classmethod
    def _initialize_traded_quote_data_manager(cls):
        cls._data_manager = TradedQuoteDataManager(ConfigurationManager.get_root_path())
        if cls._data_manager.is_connected():
            cls._initialized = True

    @classmethod
    def _initialize_backtest_manager(cls, backtest_params: dict):
        from backtest_module.backtest_manager import BacktestManager
        instance = BacktestManager()
        instance.add_backtest_params(backtest_params)
        return instance

    @classmethod
    def _initialize_execution_manager(cls):
        from execution_module.execution_manager import ExecutionManager
        return ExecutionManager()

    @classmethod
    def _initialize_backtest_data_manager(cls):
        from backtest_module.backtest_data_manager import BacktestDataManager
        return BacktestDataManager()

    @classmethod
    def create_backtest_section(cls, backtest_params: dict):
        cls._initialized_checker(sort_check=False)
        backtest_manager = cls._initialize_backtest_manager(backtest_params)
        cls._backtest_manager_list.append(backtest_manager)
        execution_manager = cls._initialize_execution_manager()
        backtest_data_manager = cls._initialize_backtest_data_manager()

        backtest_manager.backtest_data_manager = backtest_data_manager
        execution_manager.backtest_manager = backtest_manager
        backtest_data_manager.backtest_manager = backtest_manager
        backtest_manager.execution_manager = execution_manager
        backtest_data_manager.initialize()

        return backtest_manager

    @classmethod
    def get_backtest_manager_list(cls):
        return cls._backtest_manager_list

    @classmethod
    def _initialized_checker(cls, sort_check=False) -> bool:
        if not cls._initialized:
            cls._initialize_traded_quote_data_manager()
        if sort_check:
            return cls._initialized
        else:
            if not cls._initialized:
                raise Exception('InitializationManager has not been initialized')
