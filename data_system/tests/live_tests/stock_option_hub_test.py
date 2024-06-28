"""
Goal: Inject the live data into the stock option hub and test the data processing pipeline
"""
import json
import threading
import time

from data_system._enums import EquityDomain
from data_system.connection.live_stream.kafka_consumer import StreamReceiverConsumer
from data_system.connection.live_stream.kafka_handler import KafkaHandler
from data_system.hub import AssetDataHub
from data_system.process.domain_distributors import AssetDistributor
from data_system.process.pipelines.equity_data_pipeline_factory import (
    EquityDataPipelineFactory,
)


def all_snapshots(asset_hub: AssetDataHub):
    while True:
        print("Snapshot")
        assets = asset_hub.get_assets()
        for asset in assets:
            print(asset)
        print("End of snapshot")
        time.sleep(1)


def main():
    server = StreamReceiverConsumer(
        topic="TSLA_stream",
        bootstrap_servers="localhost:9092",
        max_poll_records=100,
        value_deserializer=lambda m: json.loads(m.decode("ascii")),
        auto_offset_reset="earliest",  # ,'smallest'
    )

    data_hub = AssetDataHub()
    equity_data_pipeline_factory = EquityDataPipelineFactory(data_hub)
    asset_distributor = AssetDistributor()
    stock_pipe = equity_data_pipeline_factory.create_equity_data_pipeline(
        equity_domain=EquityDomain.STOCK
    )
    option_pipe = equity_data_pipeline_factory.create_equity_data_pipeline(
        equity_domain=EquityDomain.OPTION
    )
    asset_distributor.set_data_pipeline(stock_pipe, price_type="TRADED")
    asset_distributor.set_data_pipeline(option_pipe, price_type="TRADED")

    handler = KafkaHandler(system_distributor=asset_distributor)
    server.set_handler(handler)

    server_thread = threading.Thread(target=server.run, kwargs={'verbose': True, 'slow': True})
    asset_snapshot_thread = threading.Thread(target=all_snapshots, args=(data_hub,), daemon=True)
    server_thread.start()
    asset_snapshot_thread.start()
    server_thread.join()
    asset_snapshot_thread.join()


if __name__ == "__main__":
    main()
