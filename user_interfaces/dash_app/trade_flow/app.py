import threading

import dash
from dash import html, dcc, callback, Output, Input, State
from dash.exceptions import PreventUpdate

from data_system.hub import AssetDataHub
from user_interfaces.dash_app.trade_flow.window import TradeFlowWindow
from user_interfaces.dash_app.trade_flow.data import TradeFlowData
from user_interfaces.dash_app.trade_flow.selection import TradeFlowSelection

from data_system.utils.domain_operations import parse_domain


class TradeFlowApp:
    def __init__(self, asset_data_hub: AssetDataHub, **kwargs):
        self.app = dash.Dash(__name__)
        self.selection_dash = TradeFlowSelection(self.app)
        self.asset_data_hub = asset_data_hub
        self.app_data = TradeFlowData(self.asset_data_hub)
        self.lock = threading.Lock()
        self.windows = []
        self.existed_window_keys = []
        self.app.layout = html.Div(
            [
                self.selection_dash.layout,
                html.Div(id="dynamic-panels", style={"marginTop": "20px"}, children=[]),
            ]
        )
        self.register_callbacks()

    def register_callbacks(self):
        @self.app.callback(
            Output("dynamic-panels", "children"),
            Input("submit-button", "n_clicks"),
            State("ticker-input", "value"),
            State("asset-domain-dropdown", "value"),
            State("equity-domain-dropdown", "value"),
            State("price-domain-dropdown", "value"),
            State("dynamic-panels", "children"),
            State("lag-input", "value"),
            State("time-frame-input", "value"),
            State("time-unit-dropdown", "value"),
        )
        def create_new_panel(
            n_clicks, ticker, asset, equity, price, children, lag, time_frame, time_unit
        ):
            if n_clicks > 0 and ticker and asset and equity and price:
                print(children)
                domain_chain = f"{asset}.{equity}.{price}"
                domains = parse_domain(
                    domain_chain,
                    asset_domina=True,
                    equity_domina=True,
                    price_domina=True,
                )
                key = f"{ticker}_{domain_chain}_{time_frame}_{time_unit}_{lag}"
                if key in self.existed_window_keys:
                    raise PreventUpdate
                with self.lock:
                    print("Creating new panel")
                self.existed_window_keys.append(key)
                queue_manager = self.app_data.get_lag_tracker(
                    ticker, domains, time_frame, time_unit, lag
                )
                new_window = TradeFlowWindow(
                    self.app,
                    queue_manager,
                    ticker,
                    domains,
                    time_frame,
                    time_unit,
                    lag,
                )
                self.windows.append(new_window)
                children.append(new_window.layout)
                return children
            raise PreventUpdate


    def run(self, debug=False, port=8050):
        self.app.run_server(debug=debug, port=port)
