# Massive Voting Systems

Voting systems for massive competitions

## Description

This repo implements and benchmarks different voting systems for massive competitions and tries to answer the natural question: is there a better approach?

## Benchmarking

The benchmark is done as follow:

We start by generating a random ranking on N entries, which would be their 'true' ranking.

The best voting systems should correctly infer the true ranking from the aggregation of individual rankings.

We measure how close the inferred ranking is to the true ranking when varying the number of votes and the noise on each vote.


## References

Bradley Terry Model:
- David R. Hunter (2004). *"MM algorithms for generalized Bradley-Terry models."* Ann. Statist. 32 (1) 384 - 406. https://doi.org/10.1214/aos/1079120141
- Chen, Xi and Bennett, Paul N. and Collins-Thompson, Kevyn and Horvitz, Eric (2013). *"Pairwise Ranking Aggregation in a Crowdsourced Setting."* WSDM '13: Proceedings of the sixth ACM international conference on Web search and data mining. Pages 193–202.  https://doi.org/10.1145/2433396.2433420

Graph theory:
- Joel Friedman (2004). *"A proof of Alon's second eigenvalue conjecture and related problems"* Memoirs of the American Mathematical Society. https://arxiv.org/abs/cs/0405020
- Roy, Bernard (1959). "Transitivité et connexité". C. R. Acad. Sci. Paris (in French). 249: 216–218. https://gallica.bnf.fr/ark:/12148/bpt6k3201c/f222.item


## License

[CC-BY-4.0](LICENSE)

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
