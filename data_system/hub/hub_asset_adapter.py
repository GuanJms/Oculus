"""
This class is used by ContainerManager to inject asset data into the asset data hub.
"""
from data_system.hub import AssetDataHub
from data_system.security_basics import Asset


class HubAssetAdapter:
    def __init__(self, asset_data_hub: AssetDataHub):
        self._asset_data_hub = asset_data_hub

    def inject(self, data: dict, meta: dict = None, mode: str = None):
        if mode == "live":
            return self._live_inject(data, meta)
        elif mode == "bulk" or mode is None:
            return self._bulk_inject(data, meta)

    def _live_inject(self, data, meta):
        self._asset_data_hub.inject(data, meta)

    def _bulk_inject(self, data: dict, meta):
        raise NotImplementedError("Not implemented yet")  # TODO: Implement this method
