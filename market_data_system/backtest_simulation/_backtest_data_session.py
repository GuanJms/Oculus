from typing import Optional, List

from utils.global_id import GlobalComponentIDGenerator
from initialization_module.initialization_manager import InitializationManager
from market_data_system.session._data_session import DataSession
from .._enums import OperationMode

class BacktestDataSession(DataSession):

    def __init__(self):
        super().__init__()
        self._session_type = OperationMode.BACKTEST
        self._expiration_params: dict[str, dict] = {}
        # self._quote_manager: Optional[QuoteManager] = None
        self._ticker_list: Optional[List[str]] = None

    def close(self):
        raise NotImplementedError("Method not implemented")

    @property
    def ticker_list(self):
        return self._ticker_list

    def request_advance_time(self):
        self._quote_manager.request_advance_time()

    def advance_date(self, quote_date: int, start_ms_of_day: int):
        self._quote_manager.delete_all_quote_board_list()
        self._quote_manager.request_advance_date(quote_date, start_ms_of_day)
        expiration_params = self.get_expiration_params()
        # quote_board_list = QuoteBoardFactory.create_quote_board_list(self._ticker_list, expiration_params)
        # for quote_board in quote_board_list:
        #     InitializationManager.initialize_quote_board(self._quote_manager, quote_board, reinitialize=False)

    # def _get_quote_board_list(self) -> List[QuoteBoard]:
    #     return self._quote_manager.get_quote_board_list()
    #
    # def _get_quote_board_by_ticker(self, ticker: str) -> List[QuoteBoard]:
    #     return self._quote_manager.get_quote_board_list_by_root(ticker)
    #
    # def request_quote_board(self, ticker: Optional[str] = None) -> List[QuoteBoard]:
    #     if ticker is None:
    #         return self._get_quote_board_list()
    #     else:
    #         return self._get_quote_board_by_ticker(ticker)
    #
    # def set_quote_manager(self, quote_manager: QuoteManager):
    #     self._quote_manager = quote_manager

    def set_ticker_params(self, tickers_params: dict):
        self._ticker_list = tickers_params.get("ticker_list")

    # def initialize(self, quote_manager: QuoteManager, expiration_params: dict):
    #     # DONE: modify this such that it can handle expiration_params
    #     self.set_quote_manager(quote_manager)
    #     # DONE: create quote board for each ticker
    #     quote_board_list = QuoteBoardFactory.create_quote_board_list(self._ticker_list, expiration_params)
    #     for quote_board in quote_board_list:
    #         InitializationManager.initialize_quote_board(quote_manager, quote_board, reinitialize=False)

    def get_data_session_process_status(self):
        return self._quote_manager.get_process_status()

    def get_expiration_params(self):
        return self._expiration_params

    def set_expiration_params(self, expiration_params: dict):
        self._expiration_params = expiration_params
