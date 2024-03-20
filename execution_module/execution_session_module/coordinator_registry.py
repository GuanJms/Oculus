from typing import Type

from execution_module.execution_session_module.execution_action_coordinator_session import \
    ExecutionActionCoordinator
from execution_module.execution_session_module.execution_signal_coordinator import \
    ExecutionSignalCoordinator


class CoordinatorRegistry:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(CoordinatorRegistry, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._registry = {}
        self.is_initialized = False

    def register_coordinator(self, class_name: str,
                             coordinator_session_class: Type[ExecutionSignalCoordinator] |
                                                        Type[ExecutionActionCoordinator]):
        self._registry[class_name] = coordinator_session_class

    def get_coordinator(self, class_name: str):
        return self._registry[class_name]


