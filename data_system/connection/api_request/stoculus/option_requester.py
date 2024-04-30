from ._requester import StoculusRequester
from ._request_maker import StoculusRequestMaker
import requests


class StoculusOptionRequester(StoculusRequester):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(StoculusOptionRequester, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self._prefix = 'option'

    def get_exps(self, ticker: str):
        url = self.url(endpoints=['exp'])
        request_params = StoculusRequestMaker.get_option_exps_request(ticker=ticker)
        response = requests.get(url, params=request_params)
        return self.parse_response(response)


