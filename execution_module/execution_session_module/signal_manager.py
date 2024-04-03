# from typing import Dict, List
#
# from execution_module.execution_session_module.coordinator_registry import CoordinatorRegistry
# from execution_system.sessions._execution_session import ExecutionSession
# from execution_module.execution_session_module.execution_signal import ExecutionSignal
# from execution_module.execution_session_module.execution_signal_coordinator import \
#     ExecutionSignalCoordinator
#
#
# def _create_execution_signal_coordinator(execution_signal: ExecutionSignal) -> ExecutionSignalCoordinator:
#     coordinator_registry = CoordinatorRegistry()
#     execution_signal_coordinator = coordinator_registry.get_coordinator(execution_signal.name)
#     return execution_signal_coordinator
#
#
# class ExecutionSessionSignalManager:
#     def __init__(self, execution_session: ExecutionSession):
#         self._execution_session = execution_session
#
#         # id: ExecutionSignalCoordinator.class_name -> ExecutionSignalCoordinator
#         self._execution_signal_coordinator_dict: Dict[str, ExecutionSignalCoordinator] = {}
#
#     def initialize(self, execution_signal_list: List[ExecutionSignal]):
#         for execution_signal in execution_signal_list:
#             self.initialize_execution_signal(execution_signal)
#
#     def initialize_execution_signal(self, execution_signal: ExecutionSignal):
#         signal_coordinator = _create_execution_signal_coordinator(execution_signal)
#         self._execution_signal_coordinator_dict[signal_coordinator.get_coordinator_class_name()] = signal_coordinator
#
#
#
#
#
