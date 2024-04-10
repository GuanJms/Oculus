"""
This distributor class takes the data and tag with the asset type (Asset Domain) and distribute the data into the
corresponding asset domain pipeline.
"""

from ._domain_distributor import DomainDistributor
from data_system.utils import DomainMatcher
from data_system.utils._domain_operations import parse_domain

DATAPIPELINE_MAP = {
    'get_stock_quote': StockDataPipeline
}


class AssetDistributor(DomainDistributor):

    def distribute(self, data: dict):
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

        domain_chain_str = data['domains']
        domains = parse_domain(domain_chain_str)
        domain_action_str = DomainMatcher.match_domain(domains)
        domain_action = DATAPIPELINE_MAP[domain_action_str]







