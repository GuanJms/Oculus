import threading

import dash
from dash import html, dcc, callback, Output, Input, State
from dash.exceptions import PreventUpdate

from data_system.hub import AssetDataHub
from user_interfaces.dash_app.trade_flow.iv_curve_window import TradeImpliedVolCurve
from user_interfaces.dash_app.trade_flow.option_window import OptionTradeFlowWindow
from user_interfaces.dash_app.trade_flow.stock_window import StockTradeFlowWindow
from user_interfaces.dash_app.trade_flow.data import TradeFlowData
from user_interfaces.dash_app.trade_flow.selection import TradeFlowSelection
from data_system._enums import *

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
        self.strikes = kwargs.get("strikes", [])
        self.rights = kwargs.get("rights", [])
        self.time_unit = "SECOND"
        self.app.layout = self.create_layout()

    def create_layout(self):
        lag_windows = []
        vol_windows = []
        # rolling window time frame layout for stock
        for ticker in self.tickers:
            for time_frame in self.time_frames:
                for lag in self.lags:
                    stock_domains = [AssetDomain.EQUITY, EquityDomain.STOCK, PriceDomain.TRADED]
                    queue = self.app_data.get_lag_tracker(
                        ticker, stock_domains, time_frame, self.time_unit, lag
                    )
                    if queue is None:
                        print(f"Queue is None for {ticker} {time_frame} {lag}")
                        continue

                    window = StockTradeFlowWindow(
                        self.app,
                        queue,
                        ticker,
                        stock_domains,
                        time_frame,
                        self.time_unit,
                        lag,
                        self.lock,
                    )
                    lag_windows.append(window.layout)
                    self.windows.append(window)

                    option_domains = [AssetDomain.EQUITY, EquityDomain.OPTION, PriceDomain.TRADED, OptionDomain.GREEK,
                                      ModelDomain.BLACK_SCHOLES]

                    for expiration in self.expirations:
                        for strike in self.strikes:
                            for right in self.rights:
                                option_args = {
                                    "expiration": expiration,
                                    "strike": strike,
                                    "right": right,
                                }
                                queue = self.app_data.get_lag_tracker(
                                    ticker, option_domains, time_frame, self.time_unit, lag, **option_args
                                )

                                window = OptionTradeFlowWindow(
                                    self.app,
                                    queue,
                                    ticker,
                                    option_domains,
                                    time_frame,
                                    EquityDomain.OPTION,
                                    self.time_unit,
                                    lag,
                                    self.lock,
                                    **option_args
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
