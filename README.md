# Massive Voting System

Benchmarking voting systems for massive competition

## Description

In a big competition context, a few judges cannot rank all the entries, we need a **peer review** algorithm.

Also, assigning an absolute number to an entry is quite hard, and we often need to reevaluate the number after judging a few entries. It is far easier to estimate whether an entry is better than another entry. Which leads us to **pairwise comparisons**, following other algorithms like [Gavel](https://www.anishathalye.com/2015/03/07/designing-a-better-judging-system/)

This way entries are the nodes of a directed graph where a comparison between two nodes is an arrow pointing to the better entry. We need to:
1. Design the vote in order to generate a graph with nice properties
2. Rank the entries from this network of votes.

## References

-


## License

[CC-BY-4.0](LICENSE)

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
