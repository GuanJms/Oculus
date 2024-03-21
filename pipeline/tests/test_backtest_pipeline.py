import unittest

from strategics.repo.core.strategy.extensions.oil_short_vol_strategy_rule import OilShortVolStrategyRule
from pipeline import BacktestPipeline


class TestStarter(unittest.TestCase):
    def setUp(self):
        pipeline = BacktestPipeline()
        self.pipeline = pipeline
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

        pipeline.set_params(**backtest_params)
        pipeline.set_strategy_cls(OilShortVolStrategyRule)
        pipeline.set_strategy_params(**option_strategy_params)

    def test_pipeline_run_method(self):
        self.pipeline.run()
        


if __name__ == '__main__':
    unittest.main()
