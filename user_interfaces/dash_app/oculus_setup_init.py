import json
import threading
from typing import Tuple

from data_system._enums import EquityDomain
from data_system.connection.live_stream.kafka_consumer import StreamReceiverConsumer
from data_system.connection.live_stream.kafka_handler import KafkaHandler
from data_system.hub import AssetDataHub
from data_system.process.domain_distributors import AssetDistributor
from data_system.process.pipelines.equity_data_pipeline_factory import (
    EquityDataPipelineFactory,
)
from data_system.utils.time_operations import current_date_as_int


def oculus_thread_setup(
    ticker: str,
    verbose: bool,
    slow_mode: bool = False,
    offset_reset="latest",
    slow_factor=1,
    max_poll_records=100,
    live_iv_mode=True,
    live_greek_mode=True,
    quote_date=current_date_as_int(),
):
    lock = threading.Lock()
    server = StreamReceiverConsumer(
        topic=f"{ticker}_stream_{quote_date}",
        bootstrap_servers="localhost:9092",
        max_poll_records=max_poll_records,
        value_deserializer=lambda m: json.loads(m.decode("ascii")),
        auto_offset_reset=offset_reset,
        # auto_offset_reset="earliest",  # ,'smallest'
        # auto_offset_reset="latest",  # ,'smallest'
        slow_mode=slow_mode,
        slow_factor=slow_factor,
        verbose=verbose,
    )

    data_hub = AssetDataHub(live_iv_mode=live_iv_mode, live_greek_mode=live_greek_mode)
    equity_data_pipeline_factory = EquityDataPipelineFactory(data_hub)
    asset_distributor = AssetDistributor()
    traded_stock_pipe = equity_data_pipeline_factory.create_equity_data_pipeline(
        equity_domain=EquityDomain.STOCK
    )
    traded_option_pipe = equity_data_pipeline_factory.create_equity_data_pipeline(
        equity_domain=EquityDomain.OPTION
    )
    quote_stock_pipe = equity_data_pipeline_factory.create_equity_data_pipeline(
        equity_domain=EquityDomain.STOCK
    )
    quote_option_pipe = equity_data_pipeline_factory.create_equity_data_pipeline(
        equity_domain=EquityDomain.OPTION
    )
    asset_distributor.set_data_pipeline(traded_stock_pipe, price_type="TRADED")
    asset_distributor.set_data_pipeline(traded_option_pipe, price_type="TRADED")
    asset_distributor.set_data_pipeline(quote_stock_pipe, price_type="QUOTE")
    asset_distributor.set_data_pipeline(quote_option_pipe, price_type="QUOTE")

    handler = KafkaHandler(system_distributor=asset_distributor, lock=lock)
    server.set_handler(handler)

    server_thread = threading.Thread(target=server.run)

    return server_thread, data_hub, lock
