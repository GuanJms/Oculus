from typing import Optional
from pathlib import Path
import json


class StoculusRequester:

    STOCULUS_PREFIX_MAP = {
        'timeline': 'timeline',
        'option': 'option'
    }

    API_CONFIG_PATH = Path(__file__).resolve().parent.parent / 'api_config.json'

    with open(API_CONFIG_PATH) as f:
        API_CONFIG = json.load(f)
    STOCULUS_CONFIG = API_CONFIG['STOCULUS']

    IP = STOCULUS_CONFIG['IP']
    PORT = STOCULUS_CONFIG['PORT']

    def __init__(self):
        self._prefix: Optional[str] = None

    def _url(self):
        prefix = (StoculusRequester.STOCULUS_PREFIX_MAP[self._prefix] + '/') if self._prefix else ''
        return f"http://{StoculusRequester.IP}:{StoculusRequester.PORT}/{prefix}"

    def url(self, endpoints: list[str]):
        base_url = self._url()
        endpoint_str = '/'.join(endpoints)
        return f"{base_url}{endpoint_str}/"

    @staticmethod
    def parse_response(response):
        status_code = response.status_code
        if status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Error: {status_code}")
