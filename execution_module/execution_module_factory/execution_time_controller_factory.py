from execution_module.execution_time_controller import ExecutionTimeController


class ExecutionTimeControllerFactory:

    @staticmethod
    def create_execution_time_controller():
        return ExecutionTimeController()
