import threading
from typing import List

import dash
import numpy as np
from dash import html, dcc, Output, Input, State
from dash.exceptions import PreventUpdate
from scipy.stats import gaussian_kde

# from utils.numba_optimized.sorting import fast_argsort


from data_system._enums import DomainEnum
from data_system.containers.cores import QueueManager


class TradeFlowWindow:
    def __init__(
            self,
            app: dash.Dash,
            queue_manager: QueueManager,
            ticker: str,
            domains: List[DomainEnum],
            time_frame: int,
            time_unit: str = "SECOND",
            lag: int = 0,
            lock=None,
    ):
        self.app = app
        self.queue = queue_manager
        self.ticker = ticker
        self.domains = domains
        self.time_frame = time_frame
        self.time_unit = time_unit
        self.lag = lag
        self.__id__ = f"{self.ticker}-{self.time_frame}-{self.time_unit}-{self.lag}"
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
                            id=f"size-checklist-{self.__id__}",
                            options=[
                                {"label": "Size", "value": "size"},
                                {"label": "TimeVolume", "value": "time_volume"},
                                {
                                    "label": "PriceVolumeKDE",
                                    "value": "price_volume_kde",
                                },
                                {
                                    "label": "PriceVolumeHist",
                                    "value": "price_volume_hist",
                                },
                                {
                                    "label": "QuartileOrderLogNum",
                                    "value": "quartile_order_log_number",
                                },
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
            Input(f"size-checklist-{self.__id__}", "value"),
            State(f"size-threshold-{self.__id__}", "value"),
            prevent_initial_call=True,
        )
        def update_trade_price_graph(n, checklist_value, size_threshold):

            size_plot = "size" in checklist_value
            time_volume_plot = "time_volume" in checklist_value
            price_volume_plot_kde = "price_volume_kde" in checklist_value
            price_volume_hist = "price_volume_hist" in checklist_value
            quartile_order_log_number = "quartile_order_log_number" in checklist_value
            size_required = (
                    size_plot
                    or time_volume_plot
                    or price_volume_plot_kde
                    or price_volume_hist
                    or quartile_order_log_number
            )

            if size_threshold is None:
                size_threshold = 0

            nodes = request_nodes()
            X = request_datetime(nodes)
            timestamps = request_timestamps(nodes)
            Y = request_price(nodes)
            Z = request_size(nodes)
            if size_required:
                Z_scaled = request_log_size_scaled(nodes)

            filter_mask = Z > size_threshold

            if len(filter_mask) != len(X):
                print("Filter mask length mismatch")
            X = X[filter_mask]
            Y = Y[filter_mask]
            timestamps = timestamps[filter_mask]
            Z = Z[filter_mask]
            if size_required:
                Z_scaled = Z_scaled[filter_mask]

            # Calculate density for each point
            # xy = np.vstack([filtered_timestamps, filtered_Y])
            # density = gaussian_kde(xy)(xy)
            #
            # # Normalize density to [0, 1] range for opacity
            # density_normalized = (density - density.min()) / (
            #     density.max() - density.min()
            # )
            # opacity = (
            #     1 - density_normalized
            # )  # Invert density to get lower opacity for denser areas

            if len(X) == 0:
                raise PreventUpdate

            line_plot = {
                "x": X,
                "y": Y,
                "name": "Line Plot",
                "mode": "lines",
                "showlegend": False,
            }

            # Construct the data part of the plot
            data = {
                "data": [line_plot],  # Start with the line plot
                "layout": {
                    "title": f"Price for {self.ticker}, {round(self.time_frame / 60, 2)}min - lag: {self.lag} ",
                    "xaxis": {"range": [min(X), max(X)], "title": "Time"},
                    "yaxis": {"range": [min(Y) - 0.2, max(Y) + 0.2]},
                    "autosize": True,
                    "uirevision": "true",
                    "height": 400,  # Adjust the height as needed
                    "width": 800,  # Adjust the width as needed
                },
            }

            if size_plot:
                self.add_size_scatter_plot(data, X, Y, Z_scaled)

            if time_volume_plot:
                self.add_time_volume_plot(data, X, Y, Z_scaled)

            if price_volume_plot_kde:
                self.add_price_volume_kde(data, Y, Z)

            if price_volume_hist:
                self.add_price_volume_hist_plot(data, Y, Z_scaled)

            if quartile_order_log_number:
                self.add_quartile_order_log_number_plot(data, Y, Z_scaled)

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

        def request_price(nodes):
            data = [node.price for node in nodes]
            Y = np.fromiter(data, dtype=np.float32)
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
                "line": {"width": 0.5, "color": "blue"},
            },
            "showlegend": False,
        }
        data["data"].append(scatter_plot)

    @staticmethod
    def add_time_volume_plot(data, X, Y, Z_scaled):
        density_plot = {
            "x": X,
            "y": Y,
            "name": "Density Plot",
            "type": "histogram2d",
            "colorscale": "Viridis",  # You can choose other color scales
            "showscale": True,  # Show color scale
            "xbins": {"size": 0.1},  # Adjust the size as needed for smaller bins
            "ybins": {"size": 0.1},  # Adjust the size as needed for smaller bins
        }
        data["data"].append(density_plot)

    @staticmethod
    def add_price_volume_kde(data, Y, Z):
        bin_edges = np.linspace(min(Y), max(Y), 1000)

        bin_indices = np.digitize(Y, bins=bin_edges, right=True)
        bin_sums = np.zeros(len(bin_edges) - 1)

        for i in range(1, len(bin_edges)):
            bin_sums[i - 1] = Z[bin_indices == i].sum()

        # Calculate bin centers
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        # Perform Kernel Density Estimation
        kde = gaussian_kde(bin_centers, weights=bin_sums)
        y_range = np.linspace(min(bin_centers), max(bin_centers), 1000)
        kde_values = kde(y_range)

        # Create KDE scatter plot
        kde_plot = {
            "x": kde_values,
            "y": y_range,
            "name": "KDE Plot",
            "mode": "lines",
            "line": {"color": "orange"},
            "showlegend": False,
            "xaxis": "x2",  # Use secondary x-axis
        }
        data["data"].append(kde_plot)
        data["layout"]["xaxis2"] = {"overlaying": "x", "side": "top"}

    @staticmethod
    def add_price_volume_hist_plot(data, Y, Z_scaled):
        bin_edges = np.arange(min(Y), max(Y), 0.05)

        bin_indices = np.digitize(Y, bins=bin_edges, right=True)
        bin_sums = np.zeros(len(bin_edges) - 1)

        for i in range(1, len(bin_edges)):
            bin_sums[i - 1] = Z_scaled[bin_indices == i].sum()

        # Calculate bin centers
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        # create histogram plot
        hist_plot = {
            "x": bin_sums,
            "y": bin_centers,
            "name": "Histogram Plot",
            "type": "bar",
            "orientation": "h",
            "marker": {
                "opacity": 0.4,
            },
            "showlegend": False,
            "xaxis": "x3",  # Use secondary x-axis
        }
        data["data"].append(hist_plot)
        data["layout"]["xaxis3"] = {"overlaying": "x", "side": "top"}

    @staticmethod
    def add_quartile_order_log_number_plot(data, Y, Z_scaled):
        bin_edges = np.arange(min(Y), max(Y), 0.1)
        bin_indices = np.digitize(Y, bins=bin_edges, right=True)

        # Calculate quarters
        # sorted_indices = fast_argsort(Z_scaled)
        sorted_indices = np.argsort(Z_scaled)
        quarter_length = len(Z_scaled) // 4

        quarters = [
            sorted_indices[:quarter_length],
            sorted_indices[quarter_length: 2 * quarter_length],
            sorted_indices[2 * quarter_length: 3 * quarter_length],
            sorted_indices[3 * quarter_length:],
        ]

        # print("Z_scaled", Z_scaled)
        # print("sorted_indices: ", sorted_indices)

        # Initialize bin sums for each quarter
        bin_sums = [np.zeros(len(bin_edges) - 1) for _ in range(4)]

        for q, indices in enumerate(quarters):
            for i in range(1, len(bin_edges)):
                if (
                        len(Z_scaled[indices][bin_indices[indices] == i]) > 0
                ):  # Avoid calculating mean of empty slices
                    bin_sums[q][i - 1] = len(
                        Z_scaled[indices][bin_indices[indices] == i]
                    )

        # Calculate bin centers
        bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

        # Plot each quarter and stack bars vertically
        colors = [
            "rgba(31, 119, 180, 0.6)",
            "rgba(255, 127, 14, 0.6)",
            "rgba(44, 160, 44, 0.6)",
            "rgba(214, 39, 40, 0.6)",
        ]

        for q in range(4):
            _plot = {
                "x": bin_sums[q],
                "y": bin_centers,
                "name": f"Q{q + 1}",
                "type": "bar",
                "marker": {"color": colors[q]},
                "showlegend": True,
                "xaxis": "x4",
                "orientation": "h",
            }
            data["data"].append(_plot)
        data["layout"]["xaxis4"] = {"overlaying": "x", "side": "top"}
        data["layout"]["barmode"] = "stack"
