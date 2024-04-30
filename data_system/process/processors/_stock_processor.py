from decimal import Decimal

from ._data_processor import DataProcessor
from ...utils import value_to_decimal_class

conversion_map = {
    'ms_of_day': int,
    'bid_size': int,
    'bid_exchange': int,
    'bid': Decimal,
    'bid_condition': str,  # No conversion needed, but included for completeness
    'ask_size': int,
    'ask_exchange': int,
    'ask': Decimal,
    'ask_condition': str,  # No conversion needed, but included for completeness
    'date': int,
}


class StockProcessor(DataProcessor):
    """
    Distribute the data into the asset domain pipeline.
    :param data: dictionary
        - stock data  ['date', 'ticker', 'domains', 'data', 'header']

    For eaxmple, data
    sample data ticker: TSLA
    sample data domains: EQUITY.STOCK.QUOTE
    sample data date: 20230602
    sample data length: 361
    sample header: ['', 'ms_of_day', 'bid_size', 'bid_exchange', 'bid', 'bid_condition',
    'ask_size', 'ask_exchange', 'ask', 'ask_condition', 'date']
    sample one tick data: ['0', '34200000', '4', '1', '210.01', '0', '1', '65', '210.2', '0', '20230602']
    """

    def process(self, data, **kwargs):
        header = data.get('header', [])
        date = data.get('date', None)
        ticker = data.get('ticker', None)
        price_domain = data.get('price_domain', None)
        content_rows = data.get('data', None)

        if header is None or date is None or ticker is None or price_domain is None:
            raise ValueError('Missing required data')

        # Creating a dictionary that maps headers to values
        converted_rows = []
        for row in content_rows:
            converted_row = [conversion_map[header[i]](row[i]) for i in range(len(header))
                             if header[i] in conversion_map]
            converted_rows.append(converted_row)
        data.update({'data': converted_rows})
        return data, kwargs
