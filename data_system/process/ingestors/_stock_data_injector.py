from ._data_injector import DataInjector


class StockDataInjector(DataInjector):

    def __init__(self):
        super().__init__()

    def inject(self, data: dict, **kwargs):
        # inject stock data into AssetDataHub


