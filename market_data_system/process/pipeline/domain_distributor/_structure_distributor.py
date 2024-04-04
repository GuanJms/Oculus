"""
This distributor class takes the data and tag with the structure type (Structure Domain) and distribute the data into the
corresponding structure domain pipeline.
"""

from ._domain_distributor import DomainDistributor


class StructureDistributor(DomainDistributor):
    def tag(self, data):
        pass

    def distribute(self, data):
        pass
