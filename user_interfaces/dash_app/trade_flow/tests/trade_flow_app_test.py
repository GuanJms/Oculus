import logging
import threading

from data_system._enums import ModelDomain
from data_system.utils.time_operations import current_date_as_int
from user_interfaces.dash_app.trade_flow.all_app import TradeFlowApp
from user_interfaces.dash_app.oculus_setup_init import oculus_thread_setup


# def display_asset_data(ticker, asset_hub: AssetDataHub):
#     while True:
#         stock = asset_hub.get_stock(ticker)
#         # print(f"Stock: {stock}")
#         # print(f"Stock Queue: {[ q.get_last_queue() for q in stock._price_manager._traded_time_lag_queue_manager._containers.values()]}")
#         time.sleep(1)


def main():
    ticker = "TSLA"
    verbose = False
    # slow_mode = False
    slow_mode = True
    offset_reset = "earliest"
    live_iv_mode = True
    live_greek_mode = True
    model_modes = {ModelDomain.BLACK_SCHOLES: True}
    # offset_reset = "latest"
    slow_factor = 1
    max_poll_records = 100
    quote_date = 20240628
    # quote_date = current_date_as_int()

    # Configure logging
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)  # Set to ERROR to suppress info messages

    server_thread, data_hub, shared_lock = oculus_thread_setup(
        ticker,
        verbose,
        slow_mode,
        offset_reset,
        slow_factor,
        max_poll_records,
        live_iv_mode,
        live_greek_mode,
        quote_date,
        model_modes,
    )

    trade_flow_app = TradeFlowApp(
        asset_data_hub=data_hub,
        tickers=["TSLA"],
        time_frames=[600],
        # time_frames=[600],
        lags=[0],
        # expirations=[20240705],
        expirations=[20240628],
        strikes=[200000, 197500],
        rights=["C", "P"],
        # strikes=[],
        # rights=[],
        lock=shared_lock,
    )

    trade_flow_server_thread = threading.Thread(
        target=trade_flow_app.run, kwargs={"port": 8050, "debug": False}
    )
    # display_asset_data_thread = threading.Thread(
    #     target=display_asset_data, args=(ticker, data_hub)
    # )

    # TODO: adding vol curve visualization
    # vol_cal_runtime_thread = threading.Thread(target=vol_cal_runtime, daemon=True)
    server_thread.start()
    trade_flow_server_thread.start()
    # display_asset_data_thread.start()

    server_thread.join()
    trade_flow_server_thread.join()
    # display_asset_data_thread.join()


if __name__ == "__main__":
    main()
