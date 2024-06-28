from data_system.security_basics import Stock


class StockFactory:
    @staticmethod
    def create_stock(ticker: str, **kwargs) -> Stock:
        return Stock(ticker=ticker, **kwargs)
