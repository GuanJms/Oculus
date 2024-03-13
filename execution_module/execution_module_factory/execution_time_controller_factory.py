from execution_module.execution_time_controller import ExecutionTimeController


class ExecutionTimeControllerFactory:
    execution_time_controller_dict = {}

    @classmethod
    def create_execution_time_controller(cls, time_params: dict[str, int]) -> ExecutionTimeController:
        execution_time_controller = ExecutionTimeController(time_params)
        cls.execution_time_controller_dict[execution_time_controller.id] = execution_time_controller
        return execution_time_controller
