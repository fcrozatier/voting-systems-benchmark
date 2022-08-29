from math import ceil, sqrt

from scripts.classes import Benchmark

# Todo benchmark functions 1/log(x)

#
# Inverse function VS inverse powers of two
# Benchmark(
#     lambda N, k, i: i + ceil(N / (k + 1)),
#     lambda N, k, i: i + ceil(N / 2**k),
# ).strong(100, 10_000)

# Benchmark results
# -----------------
# Sample size: 20
# F1 strongly better than F2: 100%"

#
# Inverse square root VS Inverse function
Benchmark(
    lambda N, k, i: i + ceil(N / sqrt(k + 3)),
    lambda N, k, i: i + ceil(N / (k + 1)),
    sample=10,
).strong(100, 10_000)

# Benchmark results
# -----------------
# Sample size: 20
# F1 strongly better than F2: 90.0%
# Average diameter difference when not better: 1
