from market_data_system.backtest_simulation.backtest_data_session import BacktestDataSession
from execution_module.execution_module_factory.execution_session_action_manager_factory import \
    ExecutionSessionActionManagerFactory
from execution_module.execution_module_factory.execution_session_signal_manager_factory import \
    ExecutionSessionSignalManagerFactory
from execution_module.execution_session_module.execution_session import ExecutionSession
from strategics.repo.core.strategy.strategy_rule import StrategyRule
from execution_module.execution_module_factory.execution_portfolio_session_factory import \
    ExecutionPortfolioSessionFactory
from execution_module.execution_module_factory.execution_time_controller_factory import ExecutionTimeControllerFactory


class ExecutionSessionFactory:
    @classmethod
    def create_session(cls, strategy_rule_instance: StrategyRule,
                       time_params: dict,
                       backtest_data_session: BacktestDataSession) -> ExecutionSession:
        execution_time_controller = ExecutionTimeControllerFactory.create_execution_time_controller(time_params)
        execution_portfolio = ExecutionPortfolioSessionFactory.create_execution_portfolio(strategy_rule_instance)
        execution_session = ExecutionSession(strategy_rule_instance=strategy_rule_instance,
                                             execution_time_controller=execution_time_controller,
                                             backtest_data_session=backtest_data_session,
                                             execution_portfolio_session=execution_portfolio)
        execution_session_signal_manager = ExecutionSessionSignalManagerFactory.create_execution_session_signal_manager(
            execution_session)
        execution_session_action_manager = ExecutionSessionActionManagerFactory.create_execution_session_action_manager(
            execution_session)
        execution_session.set_execution_session_signal_manager(execution_session_signal_manager)
        execution_session.set_execution_session_action_manager(execution_session_action_manager)
        return execution_session
