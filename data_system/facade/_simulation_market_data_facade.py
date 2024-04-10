from data_system.facade._market_data_facade import MarketDataFacade


class SimulationMarketDataFacade(MarketDataFacade):
    instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SimulationMarketDataFacade, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        super().__init__()
        raise NotImplementedError


