from abc import ABC, abstractmethod
from enum import Enum
from typing import Set, Optional

from utils.global_id import GlobalComponentIDGenerator
from status_module.status_info import StatusInfo


class Session(ABC):
    def __init__(self):
        self._id: Optional[str] = GlobalComponentIDGenerator.generate_unique_id(
            self.__class__.__name__, id(self)
        )

        self._statuses: Set[StatusInfo] = set()

    @property
    def id(self) -> str:
        return self._id

    @abstractmethod
    def refresh_status(self):
        pass

    def add_status(self, status_info: StatusInfo):
        self._statuses.add(status_info)

    def remove_status(self, status):
        self._statuses = {info for info in self._statuses if info.status != status}

    def get_statuses(self) -> Set[Enum]:
        return {info.status for info in self._statuses}

    def get_statuses_info(self) -> Set[StatusInfo]:
        return self._statuses
