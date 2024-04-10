from typing import Optional, TYPE_CHECKING

from data_system.backtest_simulation._backtest_data_session import BacktestDataSession
from data_system.backtest_simulation._backtest_data_session_factory import BacktestDataSessionFactory
from utils.global_id import GlobalComponentIDGenerator

if TYPE_CHECKING:
    from data_system.backtest_simulation._backtest_manager import HubAdaptor


class BacktestDataManager:

    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._backtest_manager: Optional['HubAdaptor'] = None
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

    def get_backtest_manager(self) -> 'HubAdaptor':
        return self._backtest_manager

    def set_backtest_manager(self, backtest_manager: 'HubAdaptor'):
        self._backtest_manager = backtest_manager

    def request_backtest_data_session(self) -> Optional[BacktestDataSession]:
        data_session = BacktestDataSessionFactory.create_data_session()
        self._backtest_data_session_dict[data_session.id] = data_session
        return data_session



