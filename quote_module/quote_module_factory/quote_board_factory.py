from quote_module.quote_board import QuoteBoard
from weakref import WeakValueDictionary


class QuoteBoardFactory:
    quote_board_dict: WeakValueDictionary[str, QuoteBoard] = WeakValueDictionary()  # id: QuoteBoard.id

    @classmethod
    def create_quote_board(cls, quote_board_creation_params: dict) -> QuoteBoard:
        quote_board = QuoteBoard(**quote_board_creation_params)
        cls.quote_board_dict[quote_board.id] = quote_board
        return quote_board

    @classmethod
    def create_quote_board_list(cls, ticker_list: list[str], expiration_params: dict[str, dict]) -> list[QuoteBoard]:
        quote_board_list = []
        for ticker in ticker_list:
            ticker_expiration_params = expiration_params.get(ticker, {})
            quote_board_creation_params = QuoteBoardFactory.create_simple_quote_board_params(ticker,
                                                                                             ticker_expiration_params)
            quote_board = QuoteBoardFactory.create_quote_board(quote_board_creation_params)
            quote_board_list.append(quote_board)
        return quote_board_list

    @classmethod
    def create_simple_quote_board_params(cls, root: str, expiration_params: dict) -> dict:
        quote_board_creation_params = expiration_params.copy()
        quote_board_creation_params.update({'root': root})
        return quote_board_creation_params

    @classmethod
    def create_root_only_simple_quote_board_params(cls, root: str) -> dict:
        quote_board_creation_params = {'root': root}
        return quote_board_creation_params
