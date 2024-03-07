import unittest
from execution_module.execution_manager import ExecutionManager
from strategy_module.strategy_rule import StrategyRule

class MyTestCase(unittest.TestCase):
    def create_new_execution(self):
        execution_manager = ExecutionManager()

if __name__ == '__main__':
    unittest.main()
