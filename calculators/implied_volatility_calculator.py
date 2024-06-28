from typing import Tuple, Any, Optional

import numpy as np
from scipy import optimize

from calculators.utils import black_scholes_call, black_scholes_put


class ImpliedVolatilityCalculator:
    # Runtime Optimization - result 2x faster with iv_guess
    # total_time = 0.0
    # call_count = 0

    @staticmethod
    def calculate_iv(
        s: np.float64 | float,
        k: np.float64 | float,
        t: np.float64 | float,  # time to expiration
        r: np.float64 | float,
        q: np.float64 | float,
        market_price: np.float64 | float,
        right: str,
        init_lower_bound: float = -0.01,
        init_upper_bound: float = 5,
        iv_guess: Optional[float] = None,
        band_width: float = 0.2,
    ) -> Optional[float]:
        # start_time = time.time()

        if iv_guess is not None:
            # print(f"Using IV guess: {iv_guess}")
            init_lower_bound = iv_guess - band_width
            init_upper_bound = iv_guess + band_width
        while True and init_upper_bound < 10:
            try:
                iv = optimize.brentq(
                    ImpliedVolatilityCalculator._implied_volatility_objective,
                    init_lower_bound,
                    init_upper_bound,
                    args=(right, s, k, t, r, q, market_price),
                )

                # end_time = time.time()
                # ImpliedVolatilityCalculator._update_timing(end_time - start_time)
                return iv
            except ValueError:
                init_upper_bound *= 2
                init_lower_bound *= 0.5
        # end_time = time.time()
        # ImpliedVolatilityCalculator._update_timing(end_time - start_time)
        return None

    @staticmethod
    def _implied_volatility_objective(
        sigma: np.float64,
        right: str,
        s: np.float64 | float,
        k: np.float64 | float,
        t: np.float64 | float,
        r: np.float64 | float,
        q: np.float64 | float,
        market_price: np.float64,
    ) -> float:
        if right == "C":
            return black_scholes_call(s, k, t, r, q, sigma) - market_price
        elif right == "P":
            return black_scholes_put(s, k, t, r, q, sigma) - market_price
        else:
            print(right, sigma, s, k, t, r, q, market_price)
            raise ValueError(
                "Invalid option type. Please use 'C' for call and 'P' for put."
            )

    # @staticmethod
    # def _update_timing(elapsed_time: float):
    #     ImpliedVolatilityCalculator.total_time += elapsed_time
    #     ImpliedVolatilityCalculator.call_count += 1
    #
    # @staticmethod
    # def get_average_time() -> float:
    #     if ImpliedVolatilityCalculator.call_count == 0:
    #         return 0.0
    #     return ImpliedVolatilityCalculator.total_time / ImpliedVolatilityCalculator.call_count
    #


#
# #
# test_iv = ImpliedVolatilityCalculator.calculate_iv(
#     s=181.33,
#     k=172.5,
#     t=1 / 365,
#     r=0.05,
#     q=0.0,
#     market_price=8.87,
#     right="C",
#     iv_guess=0.6419573581004718,
# )
#
# print(test_iv)

# Failed to calculate IV for node:  TradeNode(P: 13.11, timestamp: 1718977151308, size: 5, Exg:6, Cond:130, IV: None) Meta:  {'date': 20240621, 'ticker': 'TSLA', 'domains': [<AssetDomain.EQUITY: 1>, <EquityDomain.OPTION: 2>, <PriceDomain.TRADED: 1>], 'mode': 'live', 'timezone': 'US/Eastern', 'date_timestamp': 1718942400000, 'expiration': 20240621, 'strike': 170000, 'right': 'C'} Underlying price:  183.0895 Last IV:  None

# Failed to calculate IV for node:  TradeNode(P: 6.53, timestamp: 1718977659789, size: 1, Exg:22, Cond:125, IV: None) Meta:  {'date': 20240621, 'ticker': 'TSLA', 'domains': [<AssetDomain.EQUITY: 1>, <EquityDomain.OPTION: 2>, <PriceDomain.TRADED: 1>], 'mode': 'live', 'timezone': 'US/Eastern', 'date_timestamp': 1718942400000, 'expiration': 20240621, 'strike': 175000, 'right': 'C'} Underlying price:  181.3987 Last IV:  0.7178628898748353
# Different timestamps:  198
# Failed to calculate IV for node:  TradeNode(P: 6.4, timestamp: 1718977661426, size: 1, Exg:69, Cond:18, IV: None) Meta:  {'date': 20240621, 'ticker': 'TSLA', 'domains': [<AssetDomain.EQUITY: 1>, <EquityDomain.OPTION: 2>, <PriceDomain.TRADED: 1>], 'mode': 'live', 'timezone': 'US/Eastern', 'date_timestamp': 1718942400000, 'expiration': 20240621, 'strike': 175000, 'right': 'C'} Underlying price:  181.3752 Last IV:  0.7178628898748353
# Different timestamps:  19
# Intrinsic value is higher than market price -- Arbitrage opportunity 18.599999999999994 18.5 Size:  1 Strike:  200.0
# Different timestamps:  237
# Failed to calculate IV for node:  TradeNode(P: 6.45, timestamp: 1718977682160, size: 20, Exg:46, Cond:18, IV: None) Meta:  {'date': 20240621, 'ticker': 'TSLA', 'domains': [<AssetDomain.EQUITY: 1>, <EquityDomain.OPTION: 2>, <PriceDomain.TRADED: 1>], 'mode': 'live', 'timezone': 'US/Eastern', 'date_timestamp': 1718942400000, 'expiration': 20240621, 'strike': 175000, 'right': 'C'} Underlying price:  181.39 Last IV:  0.7178628898748353
# Different timestamps:  149
# Failed to calculate IV for node:  TradeNode(P: 8.87, timestamp: 1718977682457, size: 1, Exg:7, Cond:130, IV: None) Meta:  {'date': 20240621, 'ticker': 'TSLA', 'domains': [<AssetDomain.EQUITY: 1>, <EquityDomain.OPTION: 2>, <PriceDomain.TRADED: 1>], 'mode': 'live', 'timezone': 'US/Eastern', 'date_timestamp': 1718942400000, 'expiration': 20240621, 'strike': 172500, 'right': 'C'} Underlying price:  181.33 Last IV:  0.6419573581004718


# Failed to calculate IV for node:  TradeNode(P: 6.8, timestamp: 1718978450782, size: 1, Exg:60, Cond:18, IV: None) Meta:  {'date': 20240621, 'ticker': 'TSLA', 'domains': [<AssetDomain.EQUITY: 1>, <EquityDomain.OPTION: 2>, <PriceDomain.TRADED: 1>], 'mode': 'live', 'timezone': 'US/Eastern', 'date_timestamp': 1718942400000, 'expiration': 20240621, 'strike': 175000, 'right': 'C'} Underlying price:  181.7817 Last IV:  0.3308884826767033
