import dash

from dash.exceptions import PreventUpdate

from data_system.hub import AssetDataHub


class OptionPositionApp:

    def __init__(self, asset_data_hub: AssetDataHub, **kwargs):
        self.asset_data_hub = asset_data_hub
        self.tickers = kwargs.get("tickers", [])
        self.expirations = kwargs.get("expirations", [])
        self.strikes = kwargs.get("strikes", [])
        self.app = dash.Dash(__name__)
        self.app.layout = self.create_layout()

    def create_layout(self):
        option_pair_windows = []
        for ticker in self.tickers:






