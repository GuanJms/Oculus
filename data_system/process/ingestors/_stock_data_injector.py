from ._data_injector import DataInjector


class StockDataInjector(DataInjector):
    def __init__(self):
        super().__init__()

    def inject(self, data: dict, **kwargs):
        # inject stock data into AssetDataHub
        _data = data.copy()
        _stock_data = _data.pop("data")
        _stock_meta = _data
        print(f"Inject stock meta data: {_stock_meta} into AssetDataHub")
        print(f"Inject stock data: {_stock_data} into AssetDataHub")
        """
        TODO: implement the injection logic
        There should a place to set a container for the injector to inject the data into the container.
        Think about what a container should be like to enable the user case. Tracking data?
        Quote data on the data hub is instantaneous data of the point. But the container is a period? 
        Hub data has a container? Should injector class has a Updater class?
        How does the backtesting process enables the research analysis for time-series data, etc. 
        """

        return data, kwargs

