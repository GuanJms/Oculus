import numpy as np
import numba as nb
import matplotlib.pyplot as plt
import time

@nb.njit(
    ["int32[:,::1](float64[:,::1])", "int32[:,::1](float32[:,::1])"], parallel=True
)
def fast_argsort_2d_float(a):
    b = np.empty(a.shape, dtype=np.int32)
    for i in nb.prange(a.shape[0]):
        b[i, :] = np.argsort(a[i, :])
    return b

def simple_argsort(a):
    return np.argsort(a, axis=1)

# Function to measure execution time
def measure_time(func, array):
    start_time = time.time()
    func(array)
    end_time = time.time()
    return end_time - start_time

# Array sizes to test
array_sizes = [5, 100, 500, 1000]

# Record execution times
simple_times = []
fast_times = []

for size in array_sizes:
    array = np.random.rand(size, size).astype(np.float64)
    simple_times.append(measure_time(simple_argsort, array))
    fast_times.append(measure_time(fast_argsort_2d_float, array))

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(array_sizes, simple_times, label='simple_argsort')
plt.plot(array_sizes, fast_times, label='fast_argsort_2d_float')
plt.xlabel('Array size (N x N)')
plt.ylabel('Execution time (seconds)')
plt.title('Performance Comparison of Argsort Implementations')
plt.legend()
plt.grid(True)
plt.show()

"""
Conclusion:
Always use fast implementation of regardless of the sizes.
"""
