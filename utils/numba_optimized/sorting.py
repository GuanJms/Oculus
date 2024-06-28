import time

import numba as nb
import numpy as np


@nb.njit(
    ["int32[:,::1](float64[:,::1])", "int32[:,::1](float32[:,::1])"], parallel=True
)
def fast_argsort_2d_float(a):
    b = np.empty(a.shape, dtype=np.int32)
    for i in nb.prange(a.shape[0]):
        b[i, :] = np.argsort(a[i, :])
    return b


@nb.njit(["int32[:,::1](int32[:,::1])", "int32[:,::1](int64[:,::1])"], parallel=True)
def fast_argsort_2d_int(a):
    b = np.empty(a.shape, dtype=np.int32)
    for i in nb.prange(a.shape[0]):
        b[i, :] = np.argsort(a[i, :])
    return b


def fast_argsort_2d(a):
    if a.dtype == np.float32 or a.dtype == np.float64:
        return fast_argsort_2d_float(a)
    elif a.dtype == np.int32 or a.dtype == np.int64:
        return fast_argsort_2d_int(a)
    else:
        raise ValueError(f"Unsupported dtype: {a.dtype}")


@nb.njit(["int32[:,::1](float64[:])", "int32[:,::1](float32[:])"], parallel=True)
def fast_argsort_1d_float(a):
    b = np.empty(a.shape, dtype=np.int32)
    for i in nb.prange(a.shape[0]):
        b[i, :] = np.argsort(a[i, :])
    return b


    @nb.njit(["int32[:,::1](int32[:])", "int32[:,::1](int64[:])"], parallel=True)
    def fast_argsort_1d_int(a):
        b = np.empty(a.shape, dtype=np.int32)
        for i in nb.prange(a.shape[0]):
            b[i, :] = np.argsort(a[i, :])
        return b


def fast_argsort_1d(a):
    if a.dtype == np.float32 or a.dtype == np.float64:
        return fast_argsort_2d_float(a)
    elif a.dtype == np.int32 or a.dtype == np.int64:
        return fast_argsort_2d_int(a)
    else:
        raise ValueError(f"Unsupported dtype: {a.dtype}")


# Test the functions with different data types
input_array_int32 = np.random.randint(size=100, low=1000, high=1000).astype(np.int32)
input_array_int64 = np.random.randint(size=100, low=1000, high=1000).astype(np.int64)

# Measure average runtime for each input type
N = 10  # Number of times to run the tests


def measure_runtime(func, input_array, n):
    runtimes = []
    for _ in range(n):
        start_time = time.time()
        func(input_array)
        end_time = time.time()
        runtimes.append(end_time - start_time)
    return sum(runtimes) / n


avg_runtime_int32 = measure_runtime(fast_argsort_1d, input_array_int32, N)
avg_runtime_int64 = measure_runtime(fast_argsort_1d, input_array_int64, N)

print(avg_runtime_int32, avg_runtime_int64)
