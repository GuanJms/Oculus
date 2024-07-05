from typing import Tuple, Optional

import numpy as np
from scipy.stats import norm

from data_system._enums import OptionDomain


class GreekCalculator:
    @staticmethod
    def calculate_delta(
        s: np.float64 | float,
        k: np.float64 | float,
        t: np.float64 | float,  # time to expiration
        r: np.float64 | float,
        q: np.float64 | float,
        sigma: np.float64 | float,
        right: OptionDomain,
        d1: np.float64 | float = None,
    ) -> Optional[float]:
        if right == OptionDomain.CALL:
            option_type = 1
        elif right == OptionDomain.PUT:
            option_type = -1
        else:
            raise ValueError("Option type must be C or P or 1 or -1")
        d1 = GreekCalculator.calculate_d1(s, k, t, r, q, sigma) if d1 is None else d1
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
        d1: np.float64 | float = None,
    ) -> Optional[float]:
        d1 = GreekCalculator.calculate_d1(s, k, t, r, q, sigma) if d1 is None else d1
        # Calculate gamma
        gamma = np.exp(-q * t) * norm.pdf(d1) / (s * sigma * np.sqrt(t))
        return gamma

    @staticmethod
    def calculate_theta(
        s: np.float64 | float,
        k: np.float64 | float,
        t: np.float64 | float,  # time to expiration
        r: np.float64 | float,
        q: np.float64 | float,
        sigma: np.float64 | float,
        right: OptionDomain,
        d1=None,
        d2=None,
        drift_less=False,
    ):
        if right == OptionDomain.CALL:
            option_type = 1
        elif right == OptionDomain.PUT:
            option_type = -1
        else:
            raise ValueError("Option type must be C or P or 1 or -1")
        d1 = GreekCalculator.calculate_d1(s, k, t, r, q, sigma) if d1 is None else d1
        d2 = GreekCalculator.calculate_d2(d1, sigma, t) if d2 is None else d2

        if drift_less:
            theta = -s * norm.cdf(d1) * sigma / (2 * np.sqrt(t))
        else:
            theta = (
                -s * np.exp(-q * t) * norm.pdf(d1) * sigma / (2 * np.sqrt(t))
                - option_type * r * k * np.exp(-r * t) * norm.cdf(option_type * d2)
                + option_type * q * s * np.exp(-q * t) * norm.cdf(option_type * d1)
            )
        return theta

    @staticmethod
    def calculate_vega(
        s: np.float64 | float,
        k: np.float64 | float,
        t: np.float64 | float,  # time to expiration
        r: np.float64 | float,
        q: np.float64 | float,
        sigma: np.float64 | float,
        d1=None,
    ):
        d1 = GreekCalculator.calculate_d1(s, k, t, r, q, sigma) if d1 is None else d1
        vega = np.exp(-q * t) * s * np.sqrt(t) * norm.pdf(d1)
        return vega

    @staticmethod
    def calculate_vomma(
        s: np.float64 | float,
        k: np.float64 | float,
        t: np.float64 | float,  # time to expiration
        r: np.float64 | float,
        q: np.float64 | float,
        sigma: np.float64 | float,
        d1=None,
        d2=None,
    ):
        d1 = GreekCalculator.calculate_d1(s, k, t, r, q, sigma) if d1 is None else d1
        d2 = GreekCalculator.calculate_d2(d1, sigma, t) if d2 is None else d2
        vomma = s * np.exp(-q * t) * norm.pdf(d1) * np.sqrt(t) * d1 * d2 / sigma
        return vomma

    @staticmethod
    def calculate_d1(
        s: np.float64 | float,
        k: np.float64 | float,
        t: np.float64 | float,  # time to expiration
        r: np.float64 | float,
        q: np.float64 | float,
        sigma: np.float64 | float,
    ) -> Optional[float]:
        d1 = (np.log(s / k) + (r - q + 0.5 * sigma**2) * t) / (sigma * np.sqrt(t))
        return d1

    @staticmethod
    def calculate_d2(
        d1: np.float64 | float, sigma: np.float64 | float, t: np.float64 | float
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
