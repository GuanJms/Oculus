from typing import List, Optional
from abc import ABC, abstractmethod

from data_system._enums import DomainEnum, PriceDomain
from data_system.base_structure.factory.stoculus_data import StoculusTradeNodeFactory, StoculusQuoteNodeFactory
from data_system.hub.hub_asset_adapter import HubAssetAdapter
from data_system.process.ingestors._data_injector import DataInjector


class NodeDataInjector(DataInjector, ABC):
    def __init__(
        self,
        domains: List[DomainEnum] | None = None,
        hub_asset_adapter: HubAssetAdapter | None = None,
    ):
        super().__init__(domains=domains)
        self._preprocessor: Optional[
            StoculusTradeNodeFactory | StoculusQuoteNodeFactory
        ] = None
        self.set_preprocessor()
        self._hub_asset_adapter: HubAssetAdapter = hub_asset_adapter

    def set_hub_asset_injector(self, hub_asset_injector: HubAssetAdapter):
        self._hub_asset_adapter = hub_asset_injector

    def inject(self, data: dict, **kwargs):
        if not self.is_right_domains(data):
            return data, kwargs

        mode = data.get("mode", None)

        if mode == "live":
            return self._live_inject(data, **kwargs)
        elif mode == "bulk" or mode is None:
            return self._bulk_inject(data, **kwargs)

    def _live_inject(self, data, **kwargs):
        _meta, node = self._preprocess(data, mode="live")

        # inject asset data into the asset data hub
        if self._hub_asset_adapter:
            self._hub_asset_adapter.inject(data=node, meta=_meta, mode='live')

        return data, kwargs

    def _bulk_inject(self, data, **kwargs):
        # TODO: implement bulk injection - all wrong
        raise NotImplementedError("Bulk injection is not implemented")
        _meta, nodes = self._preprocess(data)

        if self.container_manager:
            self.container_manager.inject(data=nodes, meta=_meta)
        return data, kwargs

    def _preprocess(self, data: dict, mode=None):
        if mode == "live":
            return self._preprocess_live(data)
        elif mode == "bulk" or mode is None:
            return self._preprocess_bulk(data)

    def _preprocess_live(self, data: dict):
        _data = data.copy()
        _asset_data = _data.pop("data")
        _asset_contract = _data.pop("contract")
        _asset_meta = _data
        _asset_meta.update(_asset_contract)
        node = self._preprocessor.create_node_live(_asset_data, **_asset_meta)
        return _asset_meta, node

    def _preprocess_bulk(self, data: dict):
        _data = data.copy()
        _asset_data = _data.pop("data")
        _asset_meta = _data
        header = _asset_meta.get("header", [])
        if not header:
            raise ValueError("Header is missing in the asset data")
        self._preprocessor.set_header(header)
        nodes = self._preprocessor.create_nodes(_asset_data, **_asset_meta)
        # return _asset_meta, _asset_data # uncomment this line to implement bulk injection
        raise NotImplementedError("Bulk injection is not implemented")

    def set_preprocessor(self):
        if PriceDomain.TRADED in self._domains:
            self._preprocessor = StoculusTradeNodeFactory()
        elif PriceDomain.QUOTE in self._domains:
            self._preprocessor = StoculusQuoteNodeFactory()









