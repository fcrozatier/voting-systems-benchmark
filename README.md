# Voting Systems Benchmark

The problem: choosing a voting system for an event like a massive competition.

Most voting systems were not designed to deal with sparse data. This repo implements and benchmarks different voting systems for massive competitions and tries to answer the natural question: is there a better approach?

## Implemented voting systems

- [Bradley-Terry models](https://en.wikipedia.org/wiki/Bradley%E2%80%93Terry_model): different variants are considered depending on the way to pair entries.
  - Random pairing
  - Grouping entries in random cycles and pairing the adjacent ones, in order to create an underlying undirected [expander graph](https://en.wikipedia.org/wiki/Expander_graph) (Random cycles)
  - Cycling through strongly connected components, to increase the directed graph connectivity (CCZip)
  - Computing the [reachability](https://en.wikipedia.org/wiki/Reachability) of entries and pairing the ones further appart (Reachability)
  - [Crowd BT](https://pages.stern.nyu.edu/~xchen3/images/crowd_pairwise.pdf)
- [PageRank](https://en.wikipedia.org/wiki/PageRank)
  - Random pairings
  - Random cycles pairings
  - Iterative PageRank: after every N votes (cycles of pairings), the current PageRank is used to determine adjacent entries to compare
- [Schulze method](https://en.wikipedia.org/wiki/Schulze_method)
- [Majority Judgement](https://en.wikipedia.org/wiki/Majority_judgment)

## Benchmark
### Methodology

The benchmark is done as follows:

1. Generate a random ranking on N entries, representing the 'true' ranking.
2. Generate votes according to the true ranking and some amount of noise. That is, if A if ranked better than B in the true ranking, then the vote is A>B with 90% chance if we had 10% of noise.
3. Aggregate the votes and generate the computed ranking according to the voting system under consideration.
4. Evaluate the quality of the computed ranking by comparing it to the true ranking. The comparison focuses on the top 10% of entries, by measuring how many items of the true top 10% are missing from the computed top 10%. In other words, it's a measure of the relative overlap between the top 10% of the true and computed rankings. The pseudo formula for lists of size 100 is $1-|\mathrm{Top10(A)}\cap\mathrm{Top10(B)}|/10$. This `top10%` measure is a [pseudo-distance](https://en.wikipedia.org/wiki/Pseudometric_space) on lists and smaller values indicate a better match.

The best voting systems should correctly infer the true ranking from the aggregation of individual rankings.

### Parameters

The parameters used come from the real world scenario example motivating this research: the [Summer of Math Exposition](some.3b1b.co) competition (SoME3).

- 500 entries
- 15 000 votes

We also added 10% of noise for the benchmark to take into account errors.

## Results

### Bradley Terry variants

As expected the choice of pairing impacts the vote, and it turns out that optimizing for strong connectivity is a good idea:

![Bradley Terry family benchmark](./assets/Bradley%20Terry.png)

### PageRank variants

The PageRank algorithm is very sensitive to noise, but iterating helps improve the results

![PageRank family benchmark](./assets/PageRank.png)

### Schulze

The Schulze voting system is one of the better voting systems in classical situations, but it doesn't perform so well with sparse data.

![Schulze benchmark](./assets/Schulze.png)

### Majority Judgement

This one is different as people grade each individual entries instead of doing pairwise comparisons.

15000 votes on pairs do not correspond to 30000 individual votes because of entries appearing multiple times. So to be conservative a budget of 20000 votes was considered for this benchmark, which corresponds to 40 votes per entry.

Also from our surveys with 500 people grading the event or the website, for a 1-10 continuous grading scale we observed a typical spread of 1.5

![Majority Judgement benchmark](./assets/Majority%20Judgement.png)

## Conclusion

Comparing together the best pairings for each family of algorithms gives the following table:

![Overall benchmark](./assets/Overall.png)

So the more accurate voting systems are the Iterated PageRank and the Majority Judgement. However PageRank is really sensitive to noise where the Majority Judgement is much more robust.

![PageRank vs Majority Judgement benchmark](./assets/PageRank%20vs%20Majority%20Judgement.png)

So the Majority Judgement is a good fit in a massive competition setting as it is both precise and robust and allows us to expect about 85-90% of accuracy on the top 10%


## References

Majority Judgment
- Michel Balinski and Rida Laraki (2007). *A theory of measuring, electing, and ranking* Proceedings of the National Academy of Sciences. https://www.pnas.org/doi/abs/10.1073/pnas.0702634104

Bradley Terry based models:
- David R. Hunter (2004). *"MM algorithms for generalized Bradley-Terry models."* Ann. Statist. 32 (1) 384 - 406. https://doi.org/10.1214/aos/1079120141
- Chen, Xi and Bennett, Paul N. and Collins-Thompson, Kevyn and Horvitz, Eric (2013). *"Pairwise Ranking Aggregation in a Crowdsourced Setting."* WSDM '13: Proceedings of the sixth ACM international conference on Web search and data mining. Pages 193–202.  https://doi.org/10.1145/2433396.2433420

Expander graphs:
- Joel Friedman (2004). *"A proof of Alon's second eigenvalue conjecture and related problems"* Memoirs of the American Mathematical Society. https://arxiv.org/abs/cs/0405020



## License

[CC-BY-4.0](LICENSE)

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
