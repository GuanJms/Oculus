import json

from data_system.connection.api_request.stoculus._requester import StoculusRequester
from data_system.hub import AssetDataHub
from data_system.connection.api_request import StoculusRequestMaker
import urllib.request, urllib.parse
import requests


class StoculusTimelineRequester(StoculusRequester):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(StoculusTimelineRequester, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__()
        self._prefix = 'timeline'

    def start_connection(self, data_hub: AssetDataHub):
        url = self.url(endpoints=['start'])
        ticker_info = StoculusRequestMaker.get_asset_data_hub_ticker_info_starter_request(asset_data_hub=data_hub)
        data = json.dumps(ticker_info).encode('utf-8')

        params = {'hub_id': data_hub.id}
        query_string = urllib.parse.urlencode(params)
        url = f"{url}?{query_string}"
        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(req) as response:
            response_data = response.read()
            connection_data_json = json.loads(response_data)
        data_hub.public_token = connection_data_json.get('public_token', None)
        data_hub.private_key = connection_data_json.get('private_key', None)
        data_hub.set_failed_tickers(failed_tickers=connection_data_json.get('failed_tickers', None))
        data_hub.set_connection_errors(errors=connection_data_json.get('errors', None))

    def check_connection(self, data_hub: AssetDataHub):
        if data_hub.public_token is None or data_hub.private_key is None:
            raise ValueError(f"AssetDataHub {data_hub} is not connected")
        else:
            status_request = StoculusRequestMaker.get_token_status_request(public_token=data_hub.public_token,
                                                                           private_key=data_hub.private_key)
        url = self.url(endpoints=['status'])
        response = requests.get(url, params=status_request)
        return self.parse_response(response)

    def read_upto_time(self, data_hub: AssetDataHub, ms_of_day: int | float):
        if data_hub.public_token is None or data_hub.private_key is None:
            raise ValueError(f"AssetDataHub {data_hub} is not connected")
        else:
            read_request = StoculusRequestMaker.get_read_upto_time_request(data_hub=data_hub,
                                                                           ms_of_day=ms_of_day)
        url = self.url(endpoints=['time', 'next'])
        response = requests.get(url, params=read_request)
        return self.parse_response(response)

