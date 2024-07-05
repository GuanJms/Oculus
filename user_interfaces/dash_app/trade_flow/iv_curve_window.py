from dash import html, dcc, Output, Input, State
import numpy as np

from data_system._enums import OptionDomain
from data_system.security_basics import Stock
from data_system.security_basics.option_basics import OptionChain
from data_system.security_basics.option_basics.core import Option
from user_interfaces.dash_app.trade_flow.data import TradeFlowData
from scipy.interpolate import CubicSpline


class TradeImpliedVolCurve:
    def __init__(
        self,
        app,
        option_chain: OptionChain,
        expiration: int,
        ticker: str,
        app_data: "TradeFlowData",
    ):
        self.app = app
        self.strike_vols = {"P": {}, "C": {}}
        self.expiration = expiration
        self.ticker = ticker
        self.__id__ = f"{self.ticker}-{self.expiration}"
        self.layout = self.create_layout()
        self.option_chain: OptionChain = option_chain
        self.app_data = app_data
        self.register_callbacks()

    def create_layout(self):
        return html.Div(
            [
                dcc.Input(
                    id=f"strike-axis-min-{self.__id__}",
                    type="number",
                    placeholder="Min Y-axis",
                ),
                dcc.Input(
                    id=f"strike-axis-max-{self.__id__}",
                    type="number",
                    placeholder="Max Y-axis",
                ),
                dcc.Graph(id=f"implied_vol_curve-{self.__id__}"),
                dcc.Interval(
                    id=f"implied_vol_curve_interval-{self.__id__}",
                    interval=0.5 * 1000,
                    n_intervals=0,
                ),
            ]
        )

    def register_callbacks(self):
        @self.app.callback(
            Output(f"implied_vol_curve-{self.__id__}", "figure"),
            Input(f"implied_vol_curve_interval-{self.__id__}", "n_intervals"),
            [State(f"strike-axis-min-{self.__id__}", "value"), State(f"strike-axis-max-{self.__id__}", "value")]
        )
        def create_implied_vol_curve(n_intervals, min_strike, max_strike):
            if self.option_chain is None:
                self.option_chain = self.app_data.get_option_chain(
                    self.ticker, self.expiration
                )
            if self.option_chain is not None:
                self.update_strike_implied_vols()
            if self.option_chain is None:
                return None
            underlying_asset = self.option_chain.get_underlying_asset()
            if self.strike_vols is None:
                return None
            underlying_asset: Stock
            current_price = underlying_asset.get_last_traded_price()


            # Extract strike prices and implied volatilities for puts and calls
            strikes_p = np.array(list(self.strike_vols["P"].keys())) / 1000
            vols_p = np.array(list(self.strike_vols["P"].values()))

            strikes_c = np.array(list(self.strike_vols["C"].keys())) / 1000
            vols_c = np.array(list(self.strike_vols["C"].values()))

            # filter out strikes outside the range if provided

            # Polynomial fit
            if strikes_c.size < 4 or strikes_p.size < 4:
                return {
                    "data": [],
                    "layout": {
                        "title": f"Implied Volatility Curve for {self.ticker}",
                        "xaxis": {"title": "Strike Price"},
                        "yaxis": {"title": "Implied Volatility"},
                    },
                }

            sorted_indices_p = np.argsort(strikes_p)
            strikes_p_sorted = strikes_p[sorted_indices_p]
            vols_p_sorted = vols_p[sorted_indices_p]

            sorted_indices_c = np.argsort(strikes_c)
            strikes_c_sorted = strikes_c[sorted_indices_c]
            vols_c_sorted = vols_c[sorted_indices_c]

            # Replace polynomial fitting with cubic spline fitting
            cubic_spline_p = CubicSpline(strikes_p_sorted, vols_p_sorted)
            cubic_spline_c = CubicSpline(strikes_c_sorted, vols_c_sorted)

            # Generate points for the smooth curve
            strikes_p_smooth = np.linspace(
                strikes_p_sorted.min(), strikes_p_sorted.max(), 500
            )
            vols_p_smooth = cubic_spline_p(strikes_p_smooth)

            strikes_c_smooth = np.linspace(
                strikes_c_sorted.min(), strikes_c_sorted.max(), 500
            )
            vols_c_smooth = cubic_spline_c(strikes_c_smooth)

            data = [
                {
                    "x": strikes_p.tolist(),
                    "y": vols_p.tolist(),
                    "mode": "markers",
                    "name": "Put Implied Volatility",
                    "marker": {"color": "blue"},
                },
                # add a vertical line at the current price
                {
                    "x": [current_price, current_price],
                    "y": [0, 1],
                    "mode": "lines",
                    "name": "Current Price",
                    "line": {"color": "black", "dash": "dash"},
                },
                {
                    "x": strikes_p_smooth.tolist(),
                    "y": vols_p_smooth.tolist(),
                    "mode": "lines",
                    "name": "Put Volatility Curve",
                    "line": {"color": "blue"},
                },
                {
                    "x": strikes_c.tolist(),
                    "y": vols_c.tolist(),
                    "mode": "markers",
                    "name": "Call Implied Volatility",
                    "marker": {"color": "red"},
                },
                {
                    "x": strikes_c_smooth.tolist(),
                    "y": vols_c_smooth.tolist(),
                    "mode": "lines",
                    "name": "Call Volatility Curve",
                    "line": {"color": "red"},
                },
            ]

            layout = {
                "title": f"Implied Volatility Curve for {self.ticker} ({self.expiration})",
                "xaxis": {
                    "title": "Strike Price",
                },
                "yaxis": {"title": "Implied Volatility"},
                "autosize": True,
                "uirevision": "true",
                "height": 500,
                "width": 1000,
            }

            return {"data": data, "layout": layout}

    def update_strike_implied_vols(self):
        vols = {"P": {}, "C": {}}
        option_chain: OptionChain
        if self.option_chain is None:
            return
        options = self.option_chain.get_assets()
        for option in options:
            option: Option
            if option.option_type == OptionDomain.CALL:
                iv = option.get_last_traded_iv()
                if iv:
                    vols["C"][option.strike] = iv
            else:
                iv = option.get_last_traded_iv()
                if iv:
                    vols["P"][option.strike] = iv
        # print("Get Strike Implied Vols: ", vols)
        self.strike_vols = vols
