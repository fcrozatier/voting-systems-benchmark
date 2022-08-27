from math import ceil, sqrt

from scripts.classes import Benchmark

# Todo benchmark functions 1/2**x 1/x 1/log(x)

#
# 1/x+1 VS 1/2**x
# Benchmark(
#     F1=lambda N, k, i: i + ceil(N / (k + 1)),
#     F2=lambda N, k, i: i + ceil(N / 2**k),
# ).strong(100, 10_000)

# Benchmark results
# -----------------
# Sample size: 10
# F1 strongly better than F2 at 100%"

Benchmark(
    F1=lambda N, k, i: i + ceil(N / sqrt(k + 3)),
    F2=lambda N, k, i: i + ceil(N / (k + 1)),
    sample=10,
).strong(100, 10_000)
