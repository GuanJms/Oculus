from typing import Tuple, Optional

import numpy as np
from scipy.stats import norm


class GreekCalculator:
    @staticmethod
    def calculate_delta(
        s: np.float64 | float,
        k: np.float64 | float,
        t: np.float64 | float,  # time to expiration
        r: np.float64 | float,
        q: np.float64 | float,
        sigma: np.float64 | float,
        right: str,
    ) -> Optional[float]:
        if right == "C" or right == 1 or right == "c":
            option_type = 1
        elif right == "P" or right == -1 or right == "p":
            option_type = -1
        else:
            raise ValueError("Option type must be C or P or 1 or -1")
        # Calculate d1 and d2
        d1 = (np.log(s / k) + (r - q + 0.5 * sigma**2) * t) / (sigma * np.sqrt(t))

        # Calculate delta
        delta = option_type * np.exp(-q * t) * norm.cdf(option_type * d1)
        return delta

    @staticmethod
    def calculate_gamma(
        s: np.float64 | float,
        k: np.float64 | float,
        t: np.float64 | float,  # time to expiration
        r: np.float64 | float,
        q: np.float64 | float,
        sigma: np.float64 | float,
        driftless: bool = False
    ) -> Optional[float]:
        # Calculate d1 and d2
        d1 = (np.log(s / k) + (r - q + 0.5 * sigma**2) * t) / (sigma * np.sqrt(t))

        # Calculate gamma
        gamma = np.exp(-q * t) * norm.pdf(d1) / (s * sigma * np.sqrt(t))
        return gamma


    @staticmethod
    def calculate_d1(
        s: np.float64 | float,
        k: np.float64 | float,
        t: np.float64 | float,  # time to expiration
        r: np.float64 | float,
        q: np.float64 | float,
        sigma: np.float64 | float,
    ) -> Optional[float]:
        d1 = (np.log(s / k) + (r - q + 0.5 * sigma ** 2) * t) / (sigma * np.sqrt(t))
        return d1

    @staticmethod
    def calculate_d2(
        d1: np.float64 | float,
        sigma: np.float64 | float,
        t: np.float64 | float
    ) -> Optional[float]:
        d2 = d1 - sigma * np.sqrt(t)
        return d2


# # test the code
# s = 100
# k = 100
# t = 1
# r = 0.05
# q = 0.0
# sigma = 0.2
# right = "C"
# delta = GreekCalculator.calculate_delta(s, k, t, r, q, sigma, right)
# print(delta)
