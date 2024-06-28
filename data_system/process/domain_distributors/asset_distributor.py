"""
This distributor class takes the data and tag with the asset type (Asset Domain) and distribute the data into the
corresponding asset domain pipeline.
"""
from typing import Dict, Any

from ._domain_distributor import DomainDistributor
from data_system.utils import DomainMatcher
from data_system.utils.domain_operations import parse_domain
from ..pipelines import StockDataPipeline, DataPipeline
from ..._enums import EquityDomain


class AssetDistributor(DomainDistributor):
    def __init__(self):
        self.data_pipeline_map: Dict[str, DataPipeline] = {}

    def set_data_pipeline(self, data_pipeline: DataPipeline | Any, price_type):
        price_type = price_type.lower()
        if EquityDomain.STOCK in data_pipeline.domains:
            self._set_stock_data_pipeline(data_pipeline, price_type)
        elif EquityDomain.OPTION in data_pipeline.domains:
            self._set_option_data_pipeline(data_pipeline, price_type)
        else:
            raise ValueError(f"Invalid data pipeline domain: {data_pipeline.domains}")

    def _set_stock_data_pipeline(
        self, stock_data_pipeline: StockDataPipeline, price_type: str = "all"
    ):
        price_type = price_type.lower()
        if price_type == "all":
            self.data_pipeline_map["get_stock_quote"] = stock_data_pipeline
            self.data_pipeline_map["get_stock_traded"] = stock_data_pipeline
        elif price_type == "quote":
            self.data_pipeline_map["get_stock_quote"] = stock_data_pipeline
        elif price_type == "traded":
            self.data_pipeline_map["get_stock_traded"] = stock_data_pipeline
        else:
            raise ValueError(f"price type {price_type} is not supported")

    def _set_option_data_pipeline(self, option_pipe, price_type):
        price_type = price_type.lower()
        if price_type == "all":
            self.data_pipeline_map["get_option_quote"] = option_pipe
            self.data_pipeline_map["get_option_traded"] = option_pipe
        elif price_type == "quote":
            self.data_pipeline_map["get_option_quote"] = option_pipe
        elif price_type == "traded":
            self.data_pipeline_map["get_option_traded"] = option_pipe
        else:
            raise ValueError(f"price type {price_type} is not supported")

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
        data.update({"domains": domains})
        if domain_pipeline is None:
            print(f"domains {domains} is not supported")
        else:
            domain_pipeline.process(data, price_domain=domains[-1])
