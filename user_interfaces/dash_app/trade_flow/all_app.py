import threading

import dash
from dash import html, dcc, callback, Output, Input, State
from dash.exceptions import PreventUpdate

from data_system.hub import AssetDataHub
from user_interfaces.dash_app.trade_flow.iv_curve_window import TradeImpliedVolCurve
from user_interfaces.dash_app.trade_flow.window import TradeFlowWindow
from user_interfaces.dash_app.trade_flow.data import TradeFlowData
from user_interfaces.dash_app.trade_flow.selection import TradeFlowSelection

from data_system.utils.domain_operations import parse_domain


class TradeFlowApp:
    def __init__(self, asset_data_hub: AssetDataHub, **kwargs):
        self.app = dash.Dash(__name__)
        self.lock = kwargs.get("lock", None)
        self.selection_dash = TradeFlowSelection(self.app)
        self.asset_data_hub = asset_data_hub
        self.app_data = TradeFlowData(self.asset_data_hub)
        self.windows = []
        self.existed_window_keys = []
        self.tickers = kwargs.get("tickers", [])
        self.time_frames = kwargs.get("time_frames", [])
        self.lags = kwargs.get("lags", [])
        self.expirations = kwargs.get("expirations", [])
        self.time_unit = "SECOND"
        self.domain_chains = ["EQUITY.STOCK.TRADED"]
        self.app.layout = self.create_layout()

    def create_layout(self):
        lag_windows = []
        vol_windows = []
        # rolling window time frame layout
        for ticker in self.tickers:
            for time_frame in self.time_frames:
                for lag in self.lags:
                    for domain_chain in self.domain_chains:
                        domains = parse_domain(
                            domain_chain,
                            asset_domina=True,
                            equity_domina=True,
                            price_domina=True,
                        )

                        queue = self.app_data.get_lag_tracker(
                            ticker, domains, time_frame, self.time_unit, lag
                        )

                        window = TradeFlowWindow(
                            self.app,
                            queue,
                            ticker,
                            domains,
                            time_frame,
                            self.time_unit,
                            lag,
                            self.lock
                        )
                        lag_windows.append(window.layout)
                        self.windows.append(window)

        # implied volatility curve layout
        for ticker in self.tickers:
            for expiration in self.expirations:
                option_chain = self.app_data.get_option_chain(ticker, expiration)
                implied_vol_curve = TradeImpliedVolCurve(
                    self.app, option_chain, expiration, ticker, self.app_data
                )
                vol_windows.append(implied_vol_curve.layout)

        layout = html.Div(
            [
                html.Div(
                    lag_windows,
                    style={
                        "display": "flex",
                        "flex-wrap": "wrap",
                        # make it to the left of the screen
                    },
                ),
                html.Div(
                    vol_windows,
                ),
            ]
        )
        return layout

    def run(self, debug=False, port=8050, **kwargs):
        self.app.run_server(debug=debug, port=port, **kwargs)
