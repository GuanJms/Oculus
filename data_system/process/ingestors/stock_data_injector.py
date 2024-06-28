# from typing import List, Optional
#
# from ._node_data_injector import NodeDataInjector
# from data_system._enums import DomainEnum, AssetDomain, EquityDomain, PriceDomain
# from data_system.base_structure.factory.stoculus_data import (
#     StoculusQuoteNodeFactory,
#     StoculusTradeNodeFactory,
# )
# from ...hub.hub_asset_injector import HubAssetInjector
# from ...tracker import StockContainerManager
#
# # TODO: add some parent class for StockDataInjector and OptionDataInjector to remove duplication!!!
#
#
# class StockDataInjector(NodeDataInjector):
#     container_manager: Optional[StockContainerManager]
#
#     def __init__(
#         self,
#         domains: List[DomainEnum] | None = None,
#         hub_asset_injector: HubAssetInjector | None = None,
#     ):
#         super().__init__(domains=domains, hub_asset_injector=hub_asset_injector)
