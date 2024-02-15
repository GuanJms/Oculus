import unittest

from Backtest.QuotePrice import QuotePrice
from DataProcess.TradedQuoteDataManager import TradedQuoteDataManager
from Backtest.QuoteBoard import QuoteBoard
from Backtest.QuoteManager import QuoteManager
class MyTestCase(unittest.TestCase):
    def test1(self):
        config_path = 'some_path'
        ROOT = 'SPY'
        datamanager = TradedQuoteDataManager(config_path=config_path)
        spy_quote_board_params = {
            'root': ROOT,
            'quote_date': {
                'start_date': 20160101,
                'end_date': 20230101
            },
            'strike':{
                'min': 300,
                'max': 550,
                'minMoneyness': 0.5,
                'maxMoneyness': 1.5,
            },
            'maturity':{
                'min': 7,
                'max': 365
            },
        }

        spy_quote_board = QuoteBoard(**spy_quote_board_params)
        quote_manager = QuoteManager(data_manager = datamanager)
        quote_manager.add_quote_board(spy_quote_board)
        quote_manager.set_frequency(60000) # update every 60 seconds
        quote_manager.run_once() # default runs at set frequency
        transaction_quoue = quote_manager.get_transaction_queue() # get the transaction waits
        print(transaction_quoue)
        test_quote = transaction_quoue[0]

        root = test_quote['root']
        strike = test_quote['strike']
        maturity = test_quote['maturity']
        quote_time = test_quote['quote_time']
        price = test_quote['price']
        type = test_quote['quote_type']
        right = test_quote['right']

        test_quote_price = spy_quote_board.get_quote_price(root, strike, maturity, type, right)
        # test test_quote_price is QuotePrice class
        self.assertIsInstance(test_quote_price, QuotePrice)

        quote_manager.process_transaction_queue(batch_size = 50) # process the transaction queue
        new_quote_price = spy_quote_board.get_quote_price(root, strike, maturity, type, right)


        quote_manager.run_once(time_elapsed = 60000) # 60 seconds later



if __name__ == '__main__':
    unittest.main()
