# Massive Voting Systems

Voting systems for massive competitions

## Description

This repo implements and benchmarks different voting systems for massive competitions and tries to answer the natural question: is there a better approach?

## Benchmarking

The benchmark is done as follow:

We start by generating a random ranking on the N entries, which would be their 'true' ranking.

The best voting systems should correctly infer the true ranking from the aggregation of individual rankings.

To measure how good a voting system is, we measure how close the inferred ranking is to the true ranking when varying a few parameters like the total number of votes (budget) and the noise on votes - the probability that an individual vote on a pair matches their true order.


## References

-


## License

[CC-BY-4.0](LICENSE)

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
