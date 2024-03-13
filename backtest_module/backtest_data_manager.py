from typing import Optional, TYPE_CHECKING

from backtest_module.backtest_data_section import BacktestDataSection
from backtest_module.backtest_module_factory.backtest_data_section_factory import BacktestDataSectionFactory
from global_component_id_generator import GlobalComponentIDGenerator
from quote_module.quote_module_factory.quote_board_factory import QuoteBoardFactory
from quote_module.quote_module_factory.quote_manager_factory import QuoteManagerFactory

if TYPE_CHECKING:
    from backtest_module.backtest_manager import BacktestManager


class BacktestDataManager:

    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._backtest_manager: Optional['BacktestManager'] = None
        self._backtest_data_section_dict: dict[str, BacktestDataSection] = {} # id: BacktestDataSection

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

    def request_backtest_data_section(self) -> Optional[BacktestDataSection]:
        data_section = BacktestDataSectionFactory.create_section()
        self._backtest_data_section_dict[data_section.id] = data_section
        return data_section



