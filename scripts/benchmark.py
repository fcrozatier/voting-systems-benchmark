from math import ceil

from scripts.classes import Benchmark

# Todo benchmark functions 1/2**x 1/x 1/log(x)

Benchmark(
    F1=lambda N, k, i: i + ceil(N / (k + 1)),
    F2=lambda N, k, i: i + ceil(N / 2**k),
).strong(100, 10_000)
