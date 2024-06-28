from data_system.containers.container_managers._container_manager import (
    ContainerManager,
)

"""
This ContainerManager is used to manage snapshot containers.
"""

from data_system.containers.cores import Snapshot


class SnapshotManager(ContainerManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def inject(self, data, meta=None):
        # print(f"SnapshotManager inject - domains: {meta.get('domains')}")
        # print(f"SnapshotManager's own domains {self._domains}")
        # print(f"SnapshotManager data: {data}")
        for container in self._containers.values():
            if container.get_domains() == meta.get("domains"):
                container.inject(data)
                return

    def create_container(self, key, **kwargs):
        # create a Snapshot container with key
        snapshot = Snapshot(**kwargs)
        domains = kwargs.get("domains", self._domains)
        snapshot.set_domains(domains)
        self.set_container(key, snapshot)  # Update the container domains automatically

    def run_live_snapshot(self, size=1, domains=None):
        self.create_container("live_snapshot", size=size, domains=domains)

    def get_snapshot(self):
        snapshot: Snapshot = self.get_container("live_snapshot")
        return snapshot.get_snapshot()
