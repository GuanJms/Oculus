import unittest

from Backtest.QuotePrice import QuotePrice
from DataProcess.TradedQuoteDataManager import TradedQuoteDataManager
from Backtest.QuoteBoard import QuoteBoard
from Backtest.QuoteManager import QuoteManager
class MyTestCase(unittest.TestCase):
    def test_quote_manager_process(self):
        config_path = 'some_path'
        ROOT = 'SPY'
        datamanager = TradedQuoteDataManager(config_path=config_path)
        spy_quote_board_params = {
            'root': ROOT,
            'quote_date_range': {
                'start_date': 20240201,
                'end_date': 20240216,
                'current_date': 20240215
            },
            'strike_range':{
                'min': 300,
                'max': 550,
                'minMoneyness': 0.5,
                'maxMoneyness': 1.5,
            },
            'maturity_range':{
                'min': 7,
                'max': 365
            },
        }

        spy_quote_board = QuoteBoard(**spy_quote_board_params)
        quote_manager = QuoteManager(data_manager = datamanager)
        quote_manager.add_quote_board(spy_quote_board) # subscirbe the quote board to the quote manager
        quote_manager.set_frequency(60000) # update every 60 seconds
        quote_manager.test_once() # default runs at set frequency
        transaction_quoue = quote_manager._get_transaction_queue() # get the transaction waits

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

        quote_manager.process_queue() # process the transaction queue
        current_quote_price = spy_quote_board.get_quote_price(root, strike, maturity, type, right)

        quote_manager.run_once(total = 60000) # 60 seconds later



if __name__ == '__main__':
    unittest.main()
