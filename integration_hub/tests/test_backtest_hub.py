import unittest

from strategics.repo.core.strategy.extensions.oil_short_vol_strategy_rule import OilShortVolStrategyRule
from integration_hub import BacktestHub


class TestStarter(unittest.TestCase):
    def setUp(self):
        hub = BacktestHub()
        self.hub = hub
        tickers = ['USO']
        backtest_params = {
            'start_date': 20230101,
            'end_date': 20230131,
            'ticker_list': tickers,
            'frequency': 60000}

        long_call_delta = 0.1
        short_call_delta = 0.2
        long_put_delta = 0.1
        short_put_delta = 0.2
        short_term_DTE = 2
        long_term_DTE = 30
        short_term_DTE_range = (0, 7)
        long_term_DTE_range = (20, 40)

        option_strategy_params = {
            "long_call_delta": long_call_delta,
            "short_call_delta": short_call_delta,
            "long_put_delta": long_put_delta,
            "short_put_delta": short_put_delta,
            "short_term_DTE": short_term_DTE,
            "long_term_DTE": long_term_DTE,
            "short_term_DTE_range": short_term_DTE_range,
            "long_term_DTE_range": long_term_DTE_range,
        }

        self.strategy_param_set = set(option_strategy_params)

        hub.set_params(**backtest_params)
        hub.set_strategy_cls(OilShortVolStrategyRule)

    def test_hub_run_method(self):
        self.hub.run(strategy_param_set=self.strategy_param_set)


if __name__ == '__main__':
    unittest.main()
