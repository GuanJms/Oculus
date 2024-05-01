from typing import List

from ._requester import StoculusRequester
from ._request_maker import StoculusRequestMaker
import requests


class StoculusOptionRequester(StoculusRequester):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(StoculusOptionRequester, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self._cache = {}
        self._prefix = "option"

    def get_exps(self, ticker: str):
        url = self.url(endpoints=["exp"])
        request_params = StoculusRequestMaker.get_option_exps_request(ticker=ticker)
        response = requests.get(url, params=request_params)
        return self.parse_response(response)

    def get_strikes(self, ticker: str, exp: int):
        url = self.url(endpoints=["exp", "strikes"])
        request_params = StoculusRequestMaker.get_option_strikes_request(
            ticker=ticker, exp=exp
        )
        response = requests.get(url, params=request_params)
        return self.parse_response(response)

    def get_tickers(self):
        if "tickers" in self._cache:
            return self._cache["tickers"]
        url = self.url(endpoints=["tickers"])
        response = requests.get(url)
        data = self.parse_response(response)
        self._store_cache(data)
        return data

    def clean_cache(self):
        self._cache = {}

    def _store_cache(self, dict_data: dict):
        # TODO: modify such that it support other structures rather than just tickers
        if dict_data is None:
            return
        for key, value in dict_data.items():
            self._cache[key] = value
