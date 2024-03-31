from execution_system.sessions._execution_session import ExecutionSession
from _enums import OperationMode

class ExecutionSessionFactory:

    @staticmethod
    def create_session(operation_mode: OperationMode) -> ExecutionSession:
        raise NotImplementedError


    #TODO: find the connected places and refactor

    # @classmethod
    # def create_session(cls, strategy_rule_instance: StrategyRule,
    #                    time_params: dict,
    #                    backtest_data_session: BacktestDataSession) -> ExecutionSession:
    #     execution_time_controller = ExecutionTimeControllerFactory.create_execution_time_controller(time_params)
    #     execution_portfolio = ExecutionPortfolioSessionFactory.create_execution_portfolio(strategy_rule_instance)
    #     execution_session = ExecutionSession(strategy_rule_instance=strategy_rule_instance,
    #                                          execution_time_controller=execution_time_controller,
    #                                          backtest_data_session=backtest_data_session,
    #                                          execution_portfolio_session=execution_portfolio)
    #     execution_session_signal_manager = ExecutionSessionSignalManagerFactory.create_execution_session_signal_manager(
    #         execution_session)
    #     execution_session_action_manager = ExecutionSessionActionManagerFactory.create_execution_session_action_manager(
    #         execution_session)
    #     execution_session.set_execution_session_signal_manager(execution_session_signal_manager)
    #     execution_session.set_execution_session_action_manager(execution_session_action_manager)
    #     return execution_session
