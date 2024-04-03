from typing import Optional

from .sessions import ExecutionSessionFactory, ExecutionSession
from utils.global_id import GlobalComponentIDGenerator
# from initialization_module.initialization_manager import InitializationManager
from strategics.repo.core.strategy.strategy_rule import StrategyRule

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from market_data_system.backtest_simulation._backtest_manager import HubAdaptor


class ExecutionManager:

    def __init__(self, ):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._backtest_manager: Optional[HubAdaptor] = None
        self._execution_session_dict: dict[str, ExecutionSession] = {} # execution_session_id: ExecutionSession
        self._strategy_id_to_execution_session_id_dict: dict[str, str] = {}

    @property
    def id(self):
        return self._id

    def get_backtest_time_params(self):
        return self._backtest_manager.get_backtest_time_params()

    def get_backtest_ticker_params(self) -> dict:
        return self._backtest_manager.get_backtest_ticker_params()

    def get_execution_session(self, strategy_rule_instance: StrategyRule) -> Optional[ExecutionSession]:
        return self._execution_session_dict.get(strategy_rule_instance.id)

    def get_execution_session_dict(self):
        return self._execution_session_dict

    def _initialize_session(self, strategy_rule_instance: StrategyRule,
                            backtest_data_session: BacktestDataSession) -> ExecutionSession:
        time_params = self.get_backtest_time_params()
        tickers = self.get_backtest_ticker_params()

        backtest_data_session.set_ticker_params(tickers)
        expiration_params = strategy_rule_instance.export_expiration_params()
        InitializationManager.initialize_backtest_data_session(backtest_data_session, time_params, expiration_params)
        execution_session = ExecutionSessionFactory.create_session(strategy_rule_instance,
                                                                   time_params,
                                                                   backtest_data_session)
        InitializationManager.initialize_execute_session(execution_session)

        self._execution_session_dict[execution_session.id] = execution_session
        self._strategy_id_to_execution_session_id_dict[strategy_rule_instance.id] = execution_session.id
        return execution_session

    def execute_strategy(self, strategy_rule_instance: StrategyRule):
        backtest_data_session = self._backtest_manager.request_backtest_data_session()
        execution_session = self._initialize_session(strategy_rule_instance, backtest_data_session)
        execution_session.start_execution()

    def set_backtest_manager(self, backtest_manager: 'HubAdaptor'):
        self._backtest_manager = backtest_manager

    def get_backtest_manager(self) -> 'HubAdaptor':
        return self._backtest_manager


