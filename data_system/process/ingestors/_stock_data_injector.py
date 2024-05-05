from typing import List

from ._data_injector import DataInjector
from data_system._enums import DomainEnum, AssetDomain, EquityDomain
from data_system.base_structure.factory.stoculus_data import (
    StoculusOptionQuoteNodeFactory,
)


class StockDataInjector(DataInjector):
    def __init__(self, domains: List[DomainEnum] | None = None):
        super().__init__(domains=domains)
        self._preprocessor = StoculusOptionQuoteNodeFactory()

    def inject(self, data: dict, **kwargs):
        # inject stock data into AssetDataHub

        # _stock_meta: {'date': '20230602', 'ticker': 'TSLA', 'domains': 'EQUITY.STOCK.QUOTE', 'header':
        # ['', 'ms_of_day', 'bid_size', 'bid_exchange', 'bid', 'bid_condition',
        # 'ask_size', 'ask_exchange', 'ask', 'ask_condition', 'date']}
        if not self.is_right_domains(data):
            return data, kwargs

        _stock_meta, nodes = self._preprocess(data)

        if self.container_manager:
            self.container_manager.inject(data=nodes, meta=_stock_meta, **kwargs)
        return data, kwargs

    def _preprocess(self, data: dict):
        _data = data.copy()
        _stock_data = _data.pop("data")
        _stock_meta = _data
        header = _stock_meta.get("header", [])
        if not header:
            raise ValueError("Header is missing in the stock data")
        self._preprocessor.set_header(header)
        nodes = self._preprocessor.create_nodes(_stock_data, **_stock_meta)

        print(f"Inject stock meta data: {_stock_meta} into StockContainerManager")
        print(f"Inject stock data: {_stock_data} into StockContainerManager")
        print(f"Inject stock nodes: {nodes} into StockContainerManager")

        return _stock_meta, _stock_data
