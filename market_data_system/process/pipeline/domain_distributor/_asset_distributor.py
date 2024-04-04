"""
This distributor class takes the data and tag with the asset type (Asset Domain) and distribute the data into the
corresponding asset domain pipeline.
"""

from ._domain_distributor import DomainDistributor


class AssetDistributor(DomainDistributor):
    def tag(self, data):
        pass

    def distribute(self, data):
        pass
