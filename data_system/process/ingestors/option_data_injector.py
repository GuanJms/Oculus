# from typing import List, Optional
#
# from ._data_injector import DataInjector
# from data_system._enums import DomainEnum, AssetDomain, EquityDomain, PriceDomain
# from data_system.base_structure.factory.stoculus_data import (
#     StoculusTradeNodeFactory,
#     StoculusQuoteNodeFactory,
# )
# from ...hub.hub_asset_injector import HubAssetInjector
# from ...tracker.cores.multi_ticker_container_manager import MultiTickerContainerManager
# from data_system.process.ingestors._node_data_injector import NodeDataInjector
#
#
# class OptionDataInjector(NodeDataInjector):
#     container_manager: Optional[MultiTickerContainerManager]
#     """
#     TODO: self._processor . Should there be seperate quote and trade processor
#         It is kinda confusing how trade data and quote data. And both stock and options are processed
#         in the this data injector; or pipeline.
#     """
#
#     def __init__(
#         self,
#         domains: List[DomainEnum] | None = None,
#         hub_asset_injector: HubAssetInjector | None = None,
#     ):
#         super().__init__(domains=domains, hub_asset_injector=hub_asset_injector)
#
#     def set_preprocessor(self):
#         # TODO: refactor needed to remove duplication
#         if PriceDomain.TRADED in self._domains:
#             self._preprocessor = StoculusTradeNodeFactory()
#         elif PriceDomain.QUOTE in self._domains:
#             self._preprocessor = StoculusQuoteNodeFactory()
