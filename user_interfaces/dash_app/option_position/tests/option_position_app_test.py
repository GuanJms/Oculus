from user_interfaces.dash_app.oculus_setup_init import oculus_thread_setup


def main():
    ticker = "TSLA"
    verbose = False
    slow_mode = True
    offset_reset = "earliest"
    slow_factor = 10
    max_poll_records = 100

    server_thread, data_hub = oculus_thread_setup(
        ticker,
        verbose=verbose,
        slow_mode=slow_mode,
        offset_reset=offset_reset,
        slow_factor=slow_factor,
        max_poll_records=max_poll_records,
    )

    expirations = [20240621]
    strikes = [180000, 177500, 175000, 182500, 185000, 187500]

    app_thread = OptionPositionApp(
        asset_data_hub=data_hub,
        tickers=[ticker],
        expirations=expirations,
        strikes=strikes,
    )
    server_thread.start()
