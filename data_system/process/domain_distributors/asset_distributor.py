"""
This distributor class takes the data and tag with the asset type (Asset Domain) and distribute the data into the
corresponding asset domain pipeline.
"""
from typing import Dict

from ._domain_distributor import DomainDistributor
from data_system.utils import DomainMatcher
from data_system.utils.domain_operations import parse_domain
from ..pipelines import StockDataPipeline, DataPipeline


class AssetDistributor(DomainDistributor):
    def __init__(self):
        self.data_pipeline_map: Dict[str, DataPipeline] = {}

    def set_stock_data_pipeline(self, stock_data_pipeline: StockDataPipeline):
        self.data_pipeline_map["get_stock_quote"] = stock_data_pipeline
        self.data_pipeline_map["get_stock_traded"] = stock_data_pipeline

    def get_pipeline(self, domain_action_str: str):
        return self.data_pipeline_map.get(domain_action_str, None)

    def distribute(self, data: dict):
        """
        Distribute the data into the asset domain pipeline.
        :param data: dictionary
            - stock data  ['date', 'ticker', 'domains', 'data', 'header']
        """
        if "domains" not in data:
            print("No domain information in the data")
            return
        domain_chain_str = data["domains"]
        domains = parse_domain(domain_chain_str)
        domain_action_str = DomainMatcher.match_domain(domains)
        domain_pipeline = self.get_pipeline(domain_action_str)
        if domain_pipeline is None:
            print(f"domains {domains} is not supported")
        else:
            domain_pipeline.process(data, price_domain=domains[-1])
