"""
This test is to check if the option implied volatility streaming pipeline is working properly

Results:
- Implied volatility calculation seems to be working fine
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
from data_system.security_basics.option_basics.core import Option
from calculators import ImpliedVolatilityCalculator


def all_snapshots(asset_hub: AssetDataHub):
    while True:
        print("Snapshot")
        assets = asset_hub.get_assets()
        for asset in assets:
            iv = (
                asset.get_last_traded_iv()
                if EquityDomain.OPTION in asset.domains
                else None
            )
            if iv is not None:
                print(
                    "Asset last trade price:",
                    asset,
                    "price:",
                    asset.get_last_traded_price(),
                    "IV:",
                    round(iv, 4) if iv is not None else "",
                )
        print("End of snapshot")
        time.sleep(1)
#
# This was a test to check if the iv_guess has proper optimization
# def vol_cal_runtime():
#     while True:
#         print(f"Runtime: {ImpliedVolatilityCalculator.get_average_time()}")
#         time.sleep(1)


def main():
    server = StreamReceiverConsumer(
        topic="TSLA_stream",
        bootstrap_servers="localhost:9092",
        max_poll_records=100,
        value_deserializer=lambda m: json.loads(m.decode("ascii")),
        auto_offset_reset="earliest",  # ,'smallest'
        # auto_offset_reset="latest",  # ,'smallest'
    )

    data_hub = AssetDataHub(live_iv_mode=True)
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

    server_thread = threading.Thread(
        target=server.run, kwargs={"verbose": False, "slow": False}
    )
    asset_snapshot_thread = threading.Thread(
        target=all_snapshots, args=(data_hub,), daemon=True
    )
    # TODO: adding vol curve visualization
    # vol_cal_runtime_thread = threading.Thread(target=vol_cal_runtime, daemon=True)
    server_thread.start()
    asset_snapshot_thread.start()
    # vol_cal_runtime_thread.start()
    server_thread.join()
    asset_snapshot_thread.join()
#     vol_cal_runtime_thread.join()


if __name__ == "__main__":
    main()
