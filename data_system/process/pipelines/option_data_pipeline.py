"""
Same functionality as the stock_data_pipeline.py but for options data. Please go through the stock_data_pipeline.py
"""

from ._data_pipeline import DataPipeline
from data_system._enums import EquityDomain, PriceDomain, AssetDomain
from ..ingestors import NodeDataInjector
from ..processors.option_processor import OptionProcessor


class OptionDataPipeline(DataPipeline):
    def __init__(
        self,
        steps,
        *,
        verbose=False,
        price_domain=PriceDomain.TRADED,
        hub_asset_injector=None
    ):  # TODO: implement verbose feature
        _domains = [AssetDomain.EQUITY, EquityDomain.OPTION]
        self.node_injector = NodeDataInjector(
            domains=_domains + [price_domain],
            hub_asset_adapter=hub_asset_injector,
        )
        steps = [
            ("option_data_processor", OptionProcessor()),
            ("option_data_trade_injector", self.node_injector),
        ] + steps

        super().__init__(steps, domains=_domains, verbose=verbose)

    def multi_process(self, multi_data, price_domain):
        for data in multi_data:
            self.process(data, price_domain=price_domain)

    def set_hub_injector(self, hub_asset_injector):
        self.node_injector.set_hub_asset_injector(hub_asset_injector)
        return self
