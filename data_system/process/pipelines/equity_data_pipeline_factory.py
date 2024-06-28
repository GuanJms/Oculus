from data_system._enums import EquityDomain
from data_system.hub.hub_asset_adapter import HubAssetAdapter
from data_system.process.pipelines import StockDataPipeline
from data_system.process.pipelines.option_data_pipeline import OptionDataPipeline


class EquityDataPipelineFactory:
    """
    Must set the hub asset injector before creating any equity data pipeline
    """

    def __init__(self, asset_hub):
        self.asset_hub = asset_hub  # TODO: think about if this is necessary since asset_hub is singleton
        self.hub_asset_injector = HubAssetAdapter(asset_hub)

    def create_equity_data_pipeline(
        self, equity_domain: EquityDomain, steps=None, verbose=False
    ):
        if steps is None:
            steps = []
        match equity_domain:
            case EquityDomain.STOCK:
                return StockDataPipeline(
                    steps=steps,
                    verbose=verbose,
                    hub_asset_adapter=self.hub_asset_injector,
                )
            case EquityDomain.OPTION:
                return OptionDataPipeline(
                    steps=steps,
                    verbose=verbose,
                    hub_asset_injector=self.hub_asset_injector,
                )
            case _:
                raise ValueError(f"Invalid equity domain: {equity_domain}")

    def _valid_setting(self):
        if self.hub_asset_injector is None:
            raise ValueError("Hub asset injector is not set")
