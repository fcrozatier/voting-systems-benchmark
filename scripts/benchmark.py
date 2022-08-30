from math import ceil, log, sqrt

from scripts.classes import Benchmark

# I. Inverse function VS inverse powers of two
# Benchmark(
#     lambda N, k, i: i + ceil(N / (k + 1)),
#     lambda N, k, i: i + ceil(N / 2**k),
#     sample=20,
# ).strong(100, 10_000)

# Benchmark results
# -----------------
# Sample size: 20
# F1 strongly better than F2: 100%"


# II. Inverse square root VS Inverse function
# Benchmark(
#     lambda N, k, i: i + ceil(N / (1 + sqrt(k))),
#     lambda N, k, i: i + ceil(N / (1 + k)),
#     sample=20,
# ).strong(100, 10_000)

# Benchmark results
# -----------------
# Sample size: 20
# F1 strongly better than F2: 90.0%
# Average diameter difference when not better: 1

# III. Inverse log VS Inverse square root
Benchmark(
    lambda N, k, i: i + ceil(N / (2 + log(k))),
    lambda N, k, i: i + ceil(N / (1 + sqrt(k))),
    sample=20,
).strong(500, 10_000)
