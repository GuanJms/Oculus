"""
This distributor class takes the data and tag with the asset type (Asset Domain) and distribute the data into the
corresponding asset domain pipeline.
"""

from ._domain_distributor import DomainDistributor
from data_system.utils import DomainMatcher
from data_system.utils._domain_operations import parse_domain
from ..pipelines import StockDataPipeline


class AssetDistributor(DomainDistributor):

    def __init__(self):
        self.data_pipeline_map = {'get_stock_quote': None,
                                  'get_stock_traded': None, }

    def distribute(self, data: dict):
        """
        Distribute the data into the asset domain pipeline.
        :param data: dictionary
            - stock data  ['date', 'ticker', 'domains', 'data', 'header']
        """
        if 'domains' not in data:
            print('No domain information in the data')
            return
        domain_chain_str = data['domains']
        domains = parse_domain(domain_chain_str)
        domain_action_str = DomainMatcher.match_domain(domains)
        domain_pipeline = self.data_pipeline_map[domain_action_str]
        if domain_pipeline is None:
            print(f'domains {domains} is not supported')
        else:
            domain_pipeline.process(data, price_domain=domains[-1])
