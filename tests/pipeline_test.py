import unittest

from quote_module.quote_price import QuotePrice
from data_process_module import TradedQuoteDataManager
from quote_module.quote_board import QuoteBoard
from quote_module.quote_manager import QuoteManager
class MyTestCase(unittest.TestCase):
    def test_quote_manager_process(self):
        config_path = 'config.json'
        datamanager = TradedQuoteDataManager(config_file_path=config_path)
        spy_quote_board_params = {
            'root': 'SPY',
            'strike_range':{
                'min': 300,
                'max': 550,
                'minMoneyness': 0.5,
                'maxMoneyness': 1.5,
            },
            'maturity_range':{
                'min': 7,
                'max': 365
            }
        }

        spy_quote_board = QuoteBoard(**spy_quote_board_params)
        self.assertEqual(spy_quote_board.root, 'SPY')
        quote_manager = QuoteManager(MSD_COL_NAME = 'ms_of_day') # 60 seconds
        quote_manager.connect_data_manager(data_manager=datamanager)
        backtest_setting_params ={
            'backtest_start_date' : 20240101,
            'backtest_end_date': 20240201,
            'frequency' : 60000
        }
        quote_manager.set_backtest_params(backtest_setting_params = backtest_setting_params)
        quote_manager.add_quote_board(spy_quote_board) # subscirbe the quote board to the quote manager
        self.assertEqual(quote_manager.get_quote_board_list(), [spy_quote_board])
        self.assertEqual(quote_manager.frequency, 60000) # default frequency is 60 secondss

        quote_manager._advance_time() # default runs at set frequency
        transaction_quoue = quote_manager._get_transaction_queue() # get the price waits

        test_quote = transaction_quoue

        tets_quote_params = test_quote.get_params()
        root = tets_quote_params['root']
        strike = tets_quote_params['strike']
        maturity = tets_quote_params['maturity']
        quote_time = tets_quote_params['quote_time']
        price = tets_quote_params['price']
        type = tets_quote_params['quote_type']
        right = tets_quote_params['right']

        test_quote_price = spy_quote_board.get_quote_price(root, strike, maturity, type, right)
        # test test_quote_price is QuotePrice class
        self.assertIsInstance(test_quote_price, QuotePrice)

        quote_manager._process_queue() # process the price queue # TODO: need to make this automated
        current_quote_price = spy_quote_board.get_quote_price(root, strike, maturity, type, right)

        quote_manager._advance_time(total = 60000) # 60 seconds later



if __name__ == '__main__':
    unittest.main()
