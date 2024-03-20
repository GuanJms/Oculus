from typing import Optional, TYPE_CHECKING

from backtest_module.backtest_data_session import BacktestDataSession
from backtest_module.backtest_module_factory.backtest_data_session_factory import BacktestDataSessionFactory
from global_component_id_generator import GlobalComponentIDGenerator
from quote_module.quote_module_factory.quote_board_factory import QuoteBoardFactory
from quote_module.quote_module_factory.quote_manager_factory import QuoteManagerFactory

if TYPE_CHECKING:
    from backtest_module.backtest_manager import BacktestManager


class BacktestDataManager:

    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._backtest_manager: Optional['BacktestManager'] = None
        self._backtest_data_session_dict: dict[str, BacktestDataSession] = {} # id: BacktestDataSession

    @property
    def id(self):
        return self._id

    @property
    def frequency(self):
        return self._backtest_manager.frequency

    @property
    def ticker_list(self):
        return self._backtest_manager.ticker_list

    def get_backtest_manager(self) -> 'BacktestManager':
        return self._backtest_manager

    def set_backtest_manager(self, backtest_manager: 'BacktestManager'):
        self._backtest_manager = backtest_manager

    def request_backtest_data_session(self) -> Optional[BacktestDataSession]:
        data_session = BacktestDataSessionFactory.create_session()
        self._backtest_data_session_dict[data_session.id] = data_session
        return data_session



