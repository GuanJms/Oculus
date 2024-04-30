from data_system._enums import PriceDomain
from data_system.security_basics import Asset


class StoculusRequestMaker:

    @staticmethod
    def get_asset_connection_request(asset: Asset, date: int) -> dict:
        ticker_info = {
            'DOMAINS': asset.get_domain_chain_str(price_domain=PriceDomain.QUOTE),
            'DATE': date,
        }
        return {asset.ticker : ticker_info}

    @staticmethod
    def get_assets_connection_request(assets: list[Asset], date: int) -> dict:
        request = {}
        for asset in assets:
            request.update(StoculusRequestMaker.get_asset_connection_request(asset, date))
        return request

    @staticmethod
    def get_asset_data_hub_ticker_info_starter_request(asset_data_hub: 'AssetDataHub'):
        assets = asset_data_hub.get_assets()
        timeline = asset_data_hub.get_timeline()
        date = timeline.get_date()
        ticker_info = StoculusRequestMaker.get_assets_connection_request(assets, date)
        return ticker_info

    @staticmethod
    def get_token_status_request(public_token: str, private_key: str) -> dict:
        return {'public_token': public_token, 'private_key': private_key}

    @staticmethod
    def get_read_upto_time_request(data_hub: 'AssetDataHub', ms_of_day: int | float) -> dict:
        read_request = {
            'public_token': data_hub.public_token,
            'private_key': data_hub.private_key,
            'time': ms_of_day
        }
        return read_request

    @staticmethod
    def get_option_exps_request(ticker):
        return {'ticker': ticker}



