import numpy as np
from scipy.stats import norm


def black_scholes_call(
    S: np.float64,
    K: np.float64,
    T: np.float64,
    r: np.float64,
    q: np.float64,
    sigma: np.float64,
) -> np.float64:
    F = S * np.exp(r * T)
    total_vol = sigma * np.sqrt(T)
    d1 = (np.log(F / K)) / total_vol + 0.5 * total_vol
    d2 = d1 - total_vol
    return norm.cdf(d1) * S * np.exp(-q * T) - norm.cdf(d2) * K * np.exp(-r * T)


def black_scholes_put(
    S: np.float64,
    K: np.float64,
    T: np.float64,
    r: np.float64,
    q: np.float64,
    sigma: np.float64,
) -> np.float64:
    F = S * np.exp(r * T)
    total_vol = sigma * np.sqrt(T)
    d1 = (np.log(F / K)) / total_vol + 0.5 * total_vol
    d2 = d1 - total_vol
    return norm.cdf(-d2) * K * np.exp(-r * T) - norm.cdf(-d1) * S * np.exp(-q * T)
