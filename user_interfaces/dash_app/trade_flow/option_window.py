import threading
from typing import List, Dict

import dash
import numpy as np
from dash import html, dcc, Output, Input, State
from dash.exceptions import PreventUpdate
from scipy.stats import gaussian_kde

# from utils.numba_optimized.sorting import fast_argsort


from data_system._enums import DomainEnum, EquityDomain, GreekDomain
from data_system.base_structure.nodes.greek_node import GreekNode
from data_system.containers.cores import QueueManager
from data_system.utils.domain_operations import domain_to_chains


class OptionTradeFlowWindow:
    def __init__(
        self,
        app: dash.Dash,
        queue_manager: QueueManager,
        ticker: str,
        domains: List[DomainEnum],
        time_frame: int,
        asset_type: EquityDomain,
        time_unit: str = "SECOND",
        lag: int = 0,
        lock=None,
        **kwargs,
    ):
        self.app = app
        self.queue = queue_manager
        self.ticker = ticker
        self.domains = domains
        self.time_frame = time_frame
        self.time_unit = time_unit
        self.lag = lag
        self.strike = kwargs.get("strike", None)
        self.right = kwargs.get("right", None)
        self.expiration = kwargs.get("expiration", None)
        self.__id__ = f"{self.ticker}-{self.time_frame}-{self.time_unit}-{self.lag}-{asset_type.name}-{self.strike}-{self.right}-{self.expiration}"
        self.graph_id = f"live-graph-{self.__id__}"
        self.update_id = f"graph-update-{self.__id__}"
        self.layout = self.create_layout()
        self.lock: threading.Lock = lock
        self.interval = 0.5 * 1000
        if self.time_frame >= 60 * 5:
            self.interval = 10 * 1000
        self.callback_functions()

    def create_layout(self):
        return html.Div(
            [
                html.Div(
                    [
                        dcc.Input(
                            id=f"size-threshold-{self.__id__}",
                            type="number",
                            value=10,
                            style={"width": "60px", "margin-right": "10px"},
                        ),
                        dcc.Checklist(
                            id=f"greek-checklist-{self.__id__}",
                            options=[
                                {"label": "Delta", "value": "delta"},
                                {"label": "Gamma", "value": "gamma"},
                                {"label": "Vega", "value": "vega"},
                                {"label": "Theta", "value": "theta"},
                                {"label": "Vomma", "value": "vomma"},
                            ],
                            # default delta and gamma
                            value=["delta", "gamma"],
                            className="checklist-container",  # Apply the flex container class
                        ),
                        dcc.Checklist(
                            id=f"size-checklist-{self.__id__}",
                            options=[
                                {"label": "Size", "value": "size"},
                            ],
                            value=[],
                            className="checklist-container",  # Apply the flex container class
                        ),
                    ],
                    style={
                        "width": "50%",
                        "display": "flex",
                        "justify-content": "center",
                        "align-items": "center",
                    },
                ),
                dcc.Graph(id=self.graph_id, animate=False),
                dcc.Interval(id=self.update_id, interval=0.5 * 1000),
            ]
        )

    #
    def callback_functions(self):
        @self.app.callback(
            Output(self.graph_id, "figure"),
            Input(self.update_id, "n_intervals"),
            Input(f"greek-checklist-{self.__id__}", "value"),
            Input(f"size-checklist-{self.__id__}", "value"),
            State(f"size-threshold-{self.__id__}", "value"),
            prevent_initial_call=True,
        )
        def update_trade_price_graph(
            n, greek_options, functional_options, size_threshold
        ):
            size_required = size_plot = "size" in functional_options
            if size_threshold is None:
                size_threshold = 0

            nodes = request_nodes()
            X = request_datetime(nodes)
            timestamps = request_timestamps(nodes)
            Y = request_greeks(nodes, greek_options)
            Z = request_size(nodes)

            filter_mask = Z > size_threshold

            if len(filter_mask) != len(X):
                print("Filter mask length mismatch")
            X = X[filter_mask]

            # filter Y values
            for key in Y.keys():
                Y[key] = Y[key][filter_mask]

            timestamps = timestamps[filter_mask]
            Z = Z[filter_mask]
            if size_required:
                Z_scaled = request_log_size_scaled(nodes)
                Z_scaled = Z_scaled[filter_mask]

            if len(X) == 0:
                raise PreventUpdate

            line_plot_greeks = []  # Ensure this is initialized

            # Define a mapping for y-axes
            yaxis_mapping = {0: "y", 1: "y2", 2: "y3", 3: "y4", 4: "y5"}

            # Loop through each opt_domain and create a trace with a different y-axis
            for idx, opt_domain in enumerate(Y.keys()):
                if len(Y[opt_domain]) == 0:
                    raise PreventUpdate

                # Assign each trace a different y-axis
                yaxis = yaxis_mapping.get(idx, "y")

                line_plot_greek = {
                    "x": X,
                    "y": Y[opt_domain],
                    "name": f"{opt_domain.name}",
                    "mode": "lines",
                    "showlegend": True,
                    "yaxis": yaxis,
                }
                line_plot_greeks.append(line_plot_greek)

            # Layout configuration for multiple y-axes
            layout = {
                "xaxis": {"title": "X-axis Title"},
                "yaxis": {"title": "Y-axis 1 Title"},
                "yaxis2": {
                    "title": "Y-axis 2 Title",
                    "overlaying": "y",
                    "side": "right",
                },
                "yaxis3": {
                    "title": "Y-axis 3 Title",
                    "overlaying": "y",
                    "side": "left",
                    "position": 0.15,
                },
                "yaxis4": {
                    "title": "Y-axis 4 Title",
                    "overlaying": "y",
                    "side": "right",
                    "position": 0.85,
                },
                "yaxis5": {
                    "title": "Y-axis 5 Title",
                    "overlaying": "y",
                    "side": "left",
                    "position": 0.3,
                },
                "legend": {"x": 1, "y": 1},
                "autosize": True,
                "uirevision": "true",
                "height": 400,  # Adjust the height as needed
                "width": 800,  # Adjust the width as needed
                "title": f"Greek Plot - {self.ticker} - {self.time_frame} {self.time_unit} - {self.lag} - {self.strike} - {self.right} - {self.expiration}",
            }

            # Construct the data part of the plot
            data = {"data": line_plot_greeks, "layout": layout}

            if size_plot:
                self.add_size_scatter_plot(data, X, Y, Z_scaled)
            return data

        def request_nodes():
            with self.lock:
                nodes = self.queue.get_nodes()
            return nodes

        def request_datetime(nodes):
            data = [node.datetime for node in nodes]
            X = np.fromiter(
                data,
                dtype="datetime64[ms]",
            )
            return X

        def request_timestamps(nodes):
            data = [node.timestamp for node in nodes]
            timestamps = np.fromiter(
                data,
                dtype=np.int32,
            )
            return timestamps

        def request_greeks(
            nodes: List[GreekNode], greek_options: List[str]
        ) -> Dict[GreekDomain, np.array]:
            Y: Dict[GreekDomain, np.array] = {}
            for greek in greek_options:
                try:
                    domain = GreekDomain.get_greek(greek)
                    data = [getattr(node, greek) for node in nodes]
                    greek_data = np.fromiter(data, dtype=np.float32)
                    Y[domain] = greek_data
                except ValueError:
                    continue
            return Y

        def request_size(nodes):
            data = [node.size for node in nodes]
            Z = np.fromiter(data, dtype=np.int32)
            return Z

        def request_log_size_scaled(nodes):
            data = [node.log_size_scaled for node in nodes]
            Z_scaled = np.fromiter(
                data,
                dtype=np.float32,
            )
            return Z_scaled

    @staticmethod
    def add_size_scatter_plot(data, X, Y, Z_scaled):
        scatter_plot = {
            "x": X,
            "y": Y,
            "name": "Scatter Plot",
            "mode": "markers",
            "marker": {
                "size": Z_scaled,
                "opacity": 0.5,
                "line": {"width": 0.5, "color": "red"},
            },
            "showlegend": False,
        }
        data["data"].append(scatter_plot)
