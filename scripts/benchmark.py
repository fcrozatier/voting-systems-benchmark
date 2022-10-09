from math import ceil, log, sqrt

from scripts.classes import Benchmark


def inverse(N, k, i):
    if k <= 2:
        return i + ceil(N / 2**k)
    return i + ceil(N / (k + 2))


def inverseLog(N, k, i):
    if k <= 2:
        return i + ceil(N / (1 + sqrt(k)))
    return i + ceil(N / (2 + log(k)))


# I. Inverse VS inverse powers of two
# Benchmark(
#     lambda N, k, i: inverse(N,k,i),
#     lambda N, k, i: i + ceil(N / 2**k),
#     sample=10,
# ).strong(500, 1500)

# Benchmark results
# -----------------
# Sample size: 20
# Strongly better: 100.0%


# - Strategy F1 is weakly better 100.0% of the time
# - Strategy F2 is weakly better 0.0% of the time

# II. Inverse square root VS Inverse function
# Benchmark(
#     lambda N, k, i: i + ceil(N / (1 + sqrt(k))),
#     lambda N, k, i: inverse(N,k,i),
#     sample=20,
# ).strong(500, 1500)

# Benchmark results
# -----------------
# Sample size: 20
# Strongly better: 50.0%
# Average diameter difference when not better: 1


# - Strategy F1 is weakly better 82.42% of the time
# - Strategy F2 is weakly better 17.58% of the time

# III. Inverse log VS Inverse square root
# Benchmark(
#     lambda N, k, i: inverseLog(N,k,i),
#     lambda N, k, i: i + ceil(N / (1 + sqrt(k))),
#     sample=100,
# ).strong(500, 1500)

# Benchmark results
# -----------------
# Sample size: 100
# Strongly better: 47.0%
# Average diameter difference when not better: 1.0138888888888888

# - Strategy F1 is weakly better 76.32% of the time
# - Strategy F2 is weakly better 23.68% of the time


Benchmark(
    lambda N, k, i: inverseLog(N, k, i),
    lambda N, k, i: i + ceil(N / (1 + sqrt(k))),
    lambda N, k, i: inverse(N, k, i),
    lambda N, k, i: i + ceil(N / 2**k),
    sample=1,
).strong(1000, 5000)
