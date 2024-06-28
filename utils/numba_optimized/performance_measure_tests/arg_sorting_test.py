import time
import numba as nb
import numpy as np


@nb.njit("int32[:,::1](float64[:,::1])", parallel=True)
def fast_argsort_2d_float64(a):
    b = np.empty(a.shape, dtype=np.int32)
    for i in nb.prange(a.shape[0]):
        b[i, :] = np.argsort(a[i, :])
    return b

@nb.njit("int32[:,::1](float32[:,::1])", parallel=True)
def fast_argsort_2d_float32(a):
    b = np.empty(a.shape, dtype=np.int32)
    for i in nb.prange(a.shape[0]):
        b[i, :] = np.argsort(a[i, :])
    return b


@nb.njit("int32[:,::1](int64[:,::1])", parallel=True)
def fast_argsort_2d_int64(a):
    b = np.empty(a.shape, dtype=np.int32)
    for i in nb.prange(a.shape[0]):
        b[i, :] = np.argsort(a[i, :])
    return b


@nb.njit("int32[:,::1](int64[:,::1])", parallel=True)
def fast_argsort_2d_int64(a):
    b = np.empty(a.shape, dtype=np.int32)
    for i in nb.prange(a.shape[0]):
        b[i, :] = np.argsort(a[i, :])
    return b

@nb.njit(["int32[:,::1](int32[:,::1])", "int32[:,::1](int64[:,::1])"], parallel=True)
def fast_argsort_2d_int6432(a):
    b = np.empty(a.shape, dtype=np.int32)
    for i in nb.prange(a.shape[0]):
        b[i, :] = np.argsort(a[i, :])
    return b


@nb.njit(
    ["int32[:,::1](float64[:,::1])", "int32[:,::1](float32[:,::1])"], parallel=True
)
def fast_argsort_2d_float6432(a):
    b = np.empty(a.shape, dtype=np.int32)
    for i in nb.prange(a.shape[0]):
        b[i, :] = np.argsort(a[i, :])
    return b


@nb.njit("int32[:,::1](int32[:,::1])", parallel=True)
def fast_argsort_2d_int32(a):
    b = np.empty(a.shape, dtype=np.int32)
    for i in nb.prange(a.shape[0]):
        b[i, :] = np.argsort(a[i, :])
    return b


@nb.njit(parallel=True)
def fast_argsort_2d_all_parallel(a):
    b = np.empty(a.shape, dtype=np.int32)
    for i in nb.prange(a.shape[0]):
        b[i, :] = np.argsort(a[i, :])
    return b


@nb.njit
def fast_argsort_2d_all_non_parallel(a):
    b = np.empty(a.shape, dtype=np.int32)
    for i in nb.prange(a.shape[0]):
        b[i, :] = np.argsort(a[i, :])
    return b


# Prepare a large input array for testing
# 1000x1000 random float array
input_array = np.random.randint(size=(10, 10), low=0, high=10000, dtype=np.int32)
# convert integer into float
input_array_float64 = input_array.astype(np.float64)
input_array_float32 = input_array.astype(np.float32)
input_array_int64 = input_array.astype(np.int64)
# int_array_float = np.random.rand(1000,1000)
N = 100  # Number of times to run the tests


def measure_runtime(func, input_array, n):
    runtimes = []
    for _ in range(n):
        start_time = time.time()
        func(input_array)
        end_time = time.time()
        runtimes.append(end_time - start_time)
    return sum(runtimes)


def simple_argsort(a):
    return np.argsort(a, axis=1)


# Measure average runtime for each function
avg_runtime_2d = measure_runtime(fast_argsort_2d_int32, input_array, N)
avg_runtime_2d_float64 = measure_runtime(
    fast_argsort_2d_float64, input_array_float64, N
)
avg_runtime_2d_int64 = measure_runtime(fast_argsort_2d_int64, input_array_int64, N)
avg_runtime_2d_int6432 = measure_runtime(fast_argsort_2d_int6432, input_array_int64, N)

avg_runtime_2d_float32 = measure_runtime(
    fast_argsort_2d_float32, input_array_float32, N
)
avg_runtime_2d_float6432 = measure_runtime(
    fast_argsort_2d_float6432, input_array_float32, N
)
avg_runtime_2d_all_parallel = measure_runtime(
    fast_argsort_2d_all_parallel, input_array, N
)
avg_runtime_2d_all_non_parallel = measure_runtime(
    fast_argsort_2d_all_non_parallel, input_array, N
)

# Measure average runtime for the simple_argsort function
avg_runtime_simple_argsort = measure_runtime(simple_argsort, input_array, N)


print(f"Average runtime int32 for fast_argsort_2d: {avg_runtime_2d:.6f} seconds")
print(f"Average runtime int64 for fast_argsort_2d: {avg_runtime_2d_int64:.6f} seconds")
print(f"Average runtime int6432 for fast_argsort_2d: {avg_runtime_2d_int6432:.6f} seconds")
print(
    f"Average runtime float64 for fast_argsort_2d: {avg_runtime_2d_float64:.6f} seconds"
)
print(
    f"Average runtime float32 for fast_argsort_2d: {avg_runtime_2d_float32:.6f} seconds"
)
print(
    f"Average runtime float6432 for fast_argsort_2d: {avg_runtime_2d_float6432:.6f} seconds"
)
print(
    f"Average runtime for fast_argsort_2d_all_parallel: {avg_runtime_2d_all_parallel:.6f} seconds"
)
print(
    f"Average runtime for fast_argsort_2d_all_non_parallel: {avg_runtime_2d_all_non_parallel:.6f} seconds"
)
print(f"Average runtime for numpy argsort: {avg_runtime_simple_argsort:.6f} seconds")

"""
# Conclusion:
Average runtime int32 for fast_argsort_2d: 0.007037 seconds
Average runtime int64 for fast_argsort_2d: 0.007471 seconds
Average runtime int6432 for fast_argsort_2d: 0.007151 seconds
Average runtime float64 for fast_argsort_2d: 0.008199 seconds
Average runtime float32 for fast_argsort_2d: 0.007986 seconds
Average runtime float6432 for fast_argsort_2d: 0.007833 seconds
Average runtime for fast_argsort_2d_all_parallel: 0.009826 seconds
Average runtime for fast_argsort_2d_all_non_parallel: 0.043651 seconds
Average runtime for numpy argsort: 0.031450 seconds

Write function that separate the integer and float arrays but allow the user to make it int32 and int64, or float32 and float64
"""