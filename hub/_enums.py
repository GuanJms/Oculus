from enum import Enum, auto
from typing import Type


class RunningStatusType(Enum):
    ACTIVE = auto()
    INACTIVE = auto()

    def is_running(self):
        return self.value == RunningStatusType.ACTIVE


class InitializationStatusType(Enum):
    INITIATED = auto()
    UNINITIATED = auto()
    READY = auto()

    def is_initalized(self):
        return self.value == InitializationStatusType.INITIATED or self.value == InitializationStatusType.READY

    def is_ready(self):
        return self.value == InitializationStatusType.READY
