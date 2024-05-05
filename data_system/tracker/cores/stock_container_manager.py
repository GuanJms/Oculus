from data_system.tracker.cores.container_manager import ContainerManager
from data_system.tracker.cores.queue_pipeline import QueuePipeline


class StockContainerManager(ContainerManager):
    def __init__(self):
        super().__init__()

    def inject(self, data, meta, **kwargs):
        ticker = meta["ticker"]
        if not self.has_key(ticker):
            raise Exception(f"Injection failed. Container for {ticker} not found. Inappropriate setup.")
        queue_pipeline: QueuePipeline = self.get_container(ticker)
        queue_pipeline.inject(data)
