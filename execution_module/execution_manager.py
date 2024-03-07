from execution_module.execution_module_factory.execution_time_controller_factory import ExecutionTimeControllerFactory
from global_component_id_generator import GlobalComponentIDGenerator


class ExecutionManager:
    def __init__(self):
        self._id = GlobalComponentIDGenerator.generate_unique_id(self.__class__.__name__, id(self))
        self._execution_time_controller = ExecutionTimeControllerFactory.create_execution_time_controller()
        self._backtest_manager = None

    @property
    def id(self):
        return self._id

    @property
    def backtest_manager(self):
        return self._backtest_manager

    @backtest_manager.setter
    def backtest_manager(self, backtest_manager):
        self._backtest_manager = backtest_manager
