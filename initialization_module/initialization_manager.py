"""
InitializationManager is used to initialize the backtest module, execution_system module: BacktestManager, ExecutionManager,
BacktestDataManager.
"""
from typing import Optional, TYPE_CHECKING
from data_process_module import TradedQuoteDataManager
from execution_module.execution_session_module.coordinator_registry import CoordinatorRegistry
# from execution_module.execution_session_module.signal_manager import \
#     ExecutionSessionSignalManager
from quote_module.quote_module_factory.quote_manager_factory import QuoteManagerFactory
# from strategics.repo.decorator.option.selection.expiration.single_dte import SingleDTESignalGenerator, SingleDTESignalCoordinator

if TYPE_CHECKING:
    from execution_module.execution_time_controller import ExecutionTimeController
    from market_data_system.backtest_simulation._backtest_data_session import BacktestDataSession
    from market_data_system.backtest_simulation._backtest_manager import HubAdaptor
    from execution_system.execution_manager import ExecutionManager
    from execution_system.sessions._execution_session import ExecutionSession
    from quote_module.quote_board import QuoteBoard
    from quote_module.quote_manager import QuoteManager


class InitializationManager:
    _action_coordinator_dict = {}
    # _signal_coordinator_dict = {SingleDTESignalGenerator: SingleDTESignalCoordinator}
    _data_manager: Optional[TradedQuoteDataManager] = None
    _backtest_manager_list = []
    _initialized = False

    @classmethod
    def get_traded_quote_data_manager(cls) -> Optional[TradedQuoteDataManager]:
        cls._initialized_checker()
        return cls._data_manager

    @classmethod
    def _initialize_traded_quote_data_manager(cls):
        cls._data_manager = TradedQuoteDataManager(ExecutionManager.get_root_path())
        if cls._data_manager.is_connected():
            cls._initialized = True

    @classmethod
    def _initialize_backtest_manager(cls, backtest_params: dict):
        from market_data_system.backtest_simulation._backtest_manager import HubAdaptor
        instance = HubAdaptor()
        instance.add_backtest_params(backtest_params)
        return instance

    @classmethod
    def _initialize_execution_manager(cls, backtest_manager: 'HubAdaptor') -> 'ExecutionManager':
        from execution_system.execution_manager import ExecutionManager
        execution_manager = ExecutionManager()
        execution_manager.set_backtest_manager(backtest_manager)
        return execution_manager

    @classmethod
    def _initialize_backtest_data_manager(cls, backtest_manager: 'HubAdaptor'):
        from market_data_system.backtest_simulation._backtest_data_manager import BacktestDataManager
        backtest_data_manager = BacktestDataManager()
        backtest_data_manager.set_backtest_manager(backtest_manager)
        return backtest_data_manager

    @classmethod
    def create_backtest_session(cls, backtest_params: dict):
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
            cls._initialize_coordinator_registry()
        if sort_check:
            return cls._initialized
        else:
            if not cls._initialized:
                raise Exception('InitializationManager has not been initialized')

    @classmethod
    def initialize_backtest_data_session(cls, backtest_data_session: 'BacktestDataSession',
                                         backtest_time_params: dict, expiration_params: dict):
        """
        :param backtest_data_session:
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
        backtest_data_session.initialize(quote_manager, expiration_params)

    @classmethod
    def initialize_quote_manager(cls, quote_manager: 'QuoteManager', data_manager: 'TradedQuoteDataManager'
                                 , quote_date: int, start_ms_of_day: int):
        quote_manager.initialize(data_manager=data_manager, quote_date=quote_date, msd=start_ms_of_day)

    @classmethod
    def initialize_execute_session(cls, execution_session: 'ExecutionSession'):
        execution_session.initialize()

    @classmethod
    def initialize_time_controller(cls, execution_time_controller: 'ExecutionTimeController'):
        execution_time_controller.initialize()

    @classmethod
    def initialize_quote_board(cls, quote_manager: 'QuoteManager',
                               quote_board: 'QuoteBoard', reinitialize: bool = False):
        quote_manager.initialize_quote_board(quote_board, reinitialize)

    # @classmethod
    # def initialize_execution_session_signal_manager(cls, signal_manager: ExecutionSessionSignalManager,
    #                                                 execution_signal_list: List[ExecutionSignal]):
    #     signal_manager.initialize(execution_signal_list)

    @classmethod
    def initialize_execution_session_action_manager(cls, action_manager, execution_action_list):
        pass

    @classmethod
    def _initialize_coordinator_registry(cls):
        registry = CoordinatorRegistry()
        for signal_class, coordinator_session_class in cls._signal_coordinator_dict.items():
            class_name = signal_class.__name__
            registry.register_coordinator(class_name, coordinator_session_class)

        for action_class, coordinator_session_class in cls._action_coordinator_dict.items():
            action_name = action_class.name
            registry.register_coordinator(action_name, coordinator_session_class)
