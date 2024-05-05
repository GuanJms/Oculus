"""
StockDataPipeline is a class that is responsible for processing the stock data with the given processor modules.
The modules could potentially include data cleaning, data mapping, data transformation, and data storage.
For example, for current stock data for the AssetDataHub prices, there is a processor should process the data into
a data formate that Injector class can use to inject the data into AssetDataHub. The injection possibly could follow after
"""

from ._data_pipeline import DataPipeline
from data_system._enums import EquityDomain, PriceDomain, AssetDomain
from ..processors import StockProcessor
from ..ingestors import StockDataInjector


class StockDataPipeline(DataPipeline):
    """
    Distribute the data into the asset domain pipeline.
    :param data: dictionary
        - stock data  ['date', 'ticker', 'domains', 'data', 'header']

    For eaxmple, data
    sample data ticker: TSLA
    sample data domains: EQUITY.STOCK.QUOTE
    sample data date: 20230602
    sample data length: 361
    sample header: ['', 'ms_of_day', 'bid_size', 'bid_exchange', 'bid', 'bid_condition',
    'ask_size', 'ask_exchange', 'ask', 'ask_condition', 'date']
    sample one tick data: ['0', '34200000', '4', '1', '210.01', '0', '1', '65', '210.2', '0', '20230602']
    """

    def __init__(
        self, steps, *, domains=None, verbose=False
    ):  # TODO: implement verbose feature
        quote_injector = StockDataInjector(domains=[AssetDomain.EQUITY, EquityDomain.STOCK, PriceDomain.QUOTE])
        steps = [
            ("stock_data_processor", StockProcessor()),
            ("stock_data_injector", quote_injector),
        ] + steps

        super().__init__(
            steps, domains=[AssetDomain.EQUITY, EquityDomain.STOCK], verbose=verbose
        )

    def multi_process(self, multi_data, price_domain):
        for data in multi_data:
            self.process(data, price_domain=price_domain)