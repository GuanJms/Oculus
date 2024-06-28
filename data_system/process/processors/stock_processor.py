from decimal import Decimal

import numpy as np

from ._data_processor import DataProcessor
from ...utils import value_to_decimal_class
from ...utils.time_operations import get_timestamp

conversion_map = {
    "ms_of_day": int,
    "bid_size": int,
    "bid_exchange": int,
    # "bid": Decimal,
    "bid": np.float64,
    "bid_condition": str,  # No conversion needed, but included for completeness
    "ask_size": int,
    "ask_exchange": int,
    # "ask": Decimal,
    "ask": np.float64,
    "ask_condition": str,  # No conversion needed, but included for completeness
    "date": int,
    "volume": np.float64,
    "size": int,
    "condition": str,  # No conversion needed, but included for completeness
    # "price": Decimal,
    "price": np.float64,
    "exchange": int,
}

# TODO: refactor this class with OptionProcessor


class StockProcessor(DataProcessor):
    def process(self, data, **kwargs):
        mode = data.get("mode", None)
        if mode == "bulk" or mode is None:
            # different format of data
            return self._bulk_process(data, **kwargs)
        elif mode == "live":
            # data from live source is singleton; data is json
            return self._live_process(data, **kwargs)
        else:
            # pass through
            return data, kwargs

    @staticmethod
    def _live_process(data, **kwargs):
        contract = data.get("contract", None)
        if contract is None:
            return data, kwargs
        date = data.get("date", None)
        ticker = data.get("ticker", None)
        price_domain = data.get("domains", None)
        data_dict = data.get("data", None)
        if date is None or ticker is None or price_domain is None or data_dict is None:
            print("Missing required data")
            return data, kwargs

        converted_contract = {
            key: conversion_map[key](contract[key])
            for key in contract
            if key in conversion_map
        }

        converted_data = {
            key: conversion_map[key](data_dict[key])
            for key in data_dict
            if key in conversion_map
        }

        if "timezone" not in data:
            data.update({"timezone": "US/Eastern"})
        data.update(
            data=converted_data,
            contract=converted_contract,
            date_timestamp=get_timestamp(date, data["timezone"]),
        )
        return data, kwargs

    @staticmethod
    def _bulk_process(data, **kwargs):
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
        header = data.get("header", [])
        date = data.get("date", None)
        ticker = data.get("ticker", None)
        price_domain = data.get("domains", None)
        content_rows = data.get("data", None)

        if header is None or date is None or ticker is None or price_domain is None:
            raise ValueError("Missing required data")

        filtered_header = [
            header[i] for i in range(len(header)) if header[i] in conversion_map
        ]

        # Creating a dictionary that maps headers to values
        converted_rows = []
        for row in content_rows:
            converted_row = [
                conversion_map[header[i]](row[i])
                for i in range(len(header))
                if header[i] in conversion_map
            ]
            converted_rows.append(converted_row)
        if "timezone" not in data:
            data.update({"timezone": "US/Eastern"})
        data.update(
            {"data": converted_rows},
            header=filtered_header,
            date_timestamp=get_timestamp(date, data["timezone"]),
        )
        return data, kwargs
