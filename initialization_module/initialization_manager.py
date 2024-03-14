"""
InitializationManager is used to initialize the backtest module, execution module: BacktestManager, ExecutionManager,
BacktestDataManager.
"""
from typing import Optional, TYPE_CHECKING
from data_process_module.traded_quote_data_manager import TradedQuoteDataManager
from configuration_module.configuration_manager import ConfigurationManager
from global_time_generator import GlobalTimeGenerator
from quote_module.quote_module_factory.quote_manager_factory import QuoteManagerFactory

if TYPE_CHECKING:
    from execution_module.execution_time_controller import ExecutionTimeController
    from backtest_module.backtest_data_section import BacktestDataSection
    from backtest_module.backtest_manager import BacktestManager
    from execution_module.execution_manager import ExecutionManager
    from execution_module.execution_module_section.execution_section import ExecutionSection
    from quote_module.quote_board import QuoteBoard
    from quote_module.quote_manager import QuoteManager


class InitializationManager:
    _data_manager: Optional[TradedQuoteDataManager] = None
    _backtest_manager_list = []
    _initialized = False

    @classmethod
    def get_traded_quote_data_manager(cls) -> Optional[TradedQuoteDataManager]:
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
    def _initialize_execution_manager(cls, backtest_manager: 'BacktestManager') -> 'ExecutionManager':
        from execution_module.execution_manager import ExecutionManager
        execution_manager = ExecutionManager()
        execution_manager.set_backtest_manager(backtest_manager)
        return execution_manager

    @classmethod
    def _initialize_backtest_data_manager(cls, backtest_manager: 'BacktestManager'):
        from backtest_module.backtest_data_manager import BacktestDataManager
        backtest_data_manager = BacktestDataManager()
        backtest_data_manager.set_backtest_manager(backtest_manager)
        return backtest_data_manager

    @classmethod
    def create_backtest_section(cls, backtest_params: dict):
        cls._initialized_checker(sort_check=False)
        backtest_manager = cls._initialize_backtest_manager(backtest_params)
        cls._backtest_manager_list.append(backtest_manager)
        execution_manager = cls._initialize_execution_manager(backtest_manager)
        backtest_data_manager = cls._initialize_backtest_data_manager(backtest_manager)

        backtest_manager.set_execution_manager(execution_manager)
        backtest_manager.set_backtest_data_manager(backtest_data_manager)
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

    @classmethod
    def initialize_backtest_data_section(cls, backtest_data_section: 'BacktestDataSection',
                                         backtest_time_params: dict, expiration_params: dict):
        """
        :param backtest_data_section:
        :param backtest_time_params: {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'frequency': self.frequency,
            'start_ms_of_day': self.start_ms_of_day,
            'end_ms_of_day': self.end_ms_of_day
        }
        :param expiration_params:
        :return:
        """
        frequency = backtest_time_params.get('frequency', 60_000)
        start_ms_of_day = backtest_time_params.get('start_ms_of_day')
        start_date = backtest_time_params.get('start_date')
        quote_date = GlobalTimeGenerator.get_next_business_day_if_not_business_day(start_date)
        quote_manager = QuoteManagerFactory.create_quote_manager(frequency=frequency)
        data_manager = cls.get_traded_quote_data_manager()
        cls.initialize_quote_manager(quote_manager, data_manager, quote_date, start_ms_of_day)
        backtest_data_section.initialize(quote_manager, expiration_params)

    @classmethod
    def initialize_quote_manager(cls, quote_manager: 'QuoteManager', data_manager: 'TradedQuoteDataManager'
                                 , quote_date: int, start_ms_of_day: int):
        quote_manager.initialize(data_manager=data_manager, quote_date=quote_date, msd=start_ms_of_day)

    @classmethod
    def initialize_execute_section(cls, execution_section: 'ExecutionSection'):
        execution_section.initialize()

    @classmethod
    def initialize_time_controller(cls, execution_time_controller: 'ExecutionTimeController'):
        execution_time_controller.initialize()

    @classmethod
    def initialize_quote_board(cls, quote_manager: 'QuoteManager',
                               quote_board: 'QuoteBoard', reinitialize: bool = False):
        quote_manager.initialize_quote_board(quote_board, reinitialize)
