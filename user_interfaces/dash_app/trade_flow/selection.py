import dash
from dash import html, dcc, callback, Output, Input, State
from data_system._enums import *

# Enum mappings for dropdown
domain_mapping = {
    AssetDomain.EQUITY: EquityDomain,
}

price_mapping = {
    EquityDomain.STOCK: PriceDomain,
    EquityDomain.OPTION: PriceDomain,
}


class TradeFlowSelection:
    def __init__(self, app):
        self.app = app
        self.layout = self.create_layout()
        self.register_callbacks()

    def create_layout(self):
        return html.Div(
            [
                html.Div(
                    [
                        html.Label(
                            "Ticker:",
                            style={
                                "display": "inline-block",
                                "marginRight": "10px",
                                "fontSize": "20px",
                            },
                        ),
                        dcc.Input(
                            id="ticker-input",
                            type="text",
                            placeholder="Enter ticker",
                            style={
                                "display": "inline-block",
                                "width": "100px",
                                "fontSize": "20px",
                            },
                            value="TSLA",
                        ),
                        dcc.Dropdown(
                            id="asset-domain-dropdown",
                            options=[
                                {"label": domain.name, "value": domain.name}
                                for domain in AssetDomain
                            ],
                            placeholder="Asset Domain",
                            value=AssetDomain.EQUITY.name,
                            style={
                                "width": "130px",
                                "display": "inline-block",
                                "marginLeft": "20px",
                            },
                        ),
                        dcc.Dropdown(
                            id="equity-domain-dropdown",
                            placeholder="Equity Domain",
                            value=EquityDomain.STOCK.name,
                            style={
                                "width": "130px",
                                "display": "inline-block",
                                "marginLeft": "20px",
                            },
                        ),
                        dcc.Dropdown(
                            id="price-domain-dropdown",
                            placeholder="Price Domain",
                            value=PriceDomain.TRADED.name,
                            style={
                                "width": "130px",
                                "display": "inline-block",
                                "marginLeft": "20px",
                            },
                        ),
                        html.Button(
                            "Submit",
                            id="submit-button",
                            n_clicks=0,
                            style={
                                "display": "inline-block",
                                "marginLeft": "40px",
                                "fontSize": "20px",
                            },
                        ),
                    ],
                    style={"marginBottom": "20px"},
                ),
                html.Div(
                    [
                        html.Label(
                            "Trade Flow Lag Input:",
                            style={
                                "display": "inline-block",
                                "marginRight": "10px",
                                "fontSize": "20px",
                            },
                        ),
                        # integer input for lag and time frame for trade flow
                        dcc.Input(
                            id="lag-input",
                            type="number",
                            placeholder="Enter lag",
                            style={
                                "display": "inline-block",
                                "width": "150px",
                                "fontSize": "20px",
                            },
                            value=0,
                        ),
                        dcc.Input(
                            id="time-frame-input",
                            type="number",
                            placeholder="Enter time frame",
                            style={
                                "display": "inline-block",
                                "width": "150px",
                                "fontSize": "20px",
                            },
                            value=60,
                        ),
                        dcc.Dropdown(
                            id="time-unit-dropdown",
                            options=[
                                {"label": time_unit.name, "value": time_unit.name}
                                for time_unit in TimeUnit
                            ],
                            placeholder="Time Unit",
                            style={
                                "width": "130px",
                                "display": "inline-block",
                                "marginLeft": "20px",
                            },
                            value=TimeUnit.SECOND.name,
                        ),
                    ]
                ),
                html.Div(id="output", style={"marginTop": "20px"}),
                html.Div(id="output-lag", style={"marginTop": "20px"}),
            ]
        )

    def register_callbacks(self):
        @self.app.callback(
            Output("equity-domain-dropdown", "options"),
            Input("asset-domain-dropdown", "value"),
        )
        def set_equity_domain_options(selected_asset):
            if selected_asset:
                asset_enum = AssetDomain[selected_asset]
                equity_enum_class = domain_mapping.get(asset_enum)
                return [
                    {"label": domain.name, "value": domain.name}
                    for domain in equity_enum_class
                ]
            return []

        @self.app.callback(
            Output("price-domain-dropdown", "options"),
            Input("equity-domain-dropdown", "value"),
        )
        def set_price_domain_options(selected_equity):
            if selected_equity:
                equity_enum = EquityDomain[selected_equity]
                price_enum_class = price_mapping.get(equity_enum)
                return [
                    {"label": domain.name, "value": domain.name}
                    for domain in price_enum_class
                ]
            return []
