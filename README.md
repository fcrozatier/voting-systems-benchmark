# NodeRank

How to rank entries in a massive competition?

## Description

In a big competition context, a few judges cannot rank all the entries, we need a **peer review** algorithm.

Also, assigning an absolute number to an entry is quite hard, and we often need to reevaluate the number after judging a few entries. It is far easier to estimate whether an entry is better than another entry. Which leads us to **pairwise comparisons**, following other algorithms like [Gavel](https://www.anishathalye.com/2015/03/07/designing-a-better-judging-system/)

This way entries are the nodes of a directed graph where a comparison between two nodes is an arrow pointing to the better entry. We need to:
1. Design the vote in order to generate a graph with nice properties
2. Rank the entries from this network of votes.

## Principles

We want the pairing graph to have the following properties:
1. It must be **[connected](https://en.wikipedia.org/wiki/Connectivity_(graph_theory)#Connected_vertices_and_graphs)**, since otherwise some islands of entries are not, even indirectly, comparable.
2. It should have the smallest **[diameter](https://en.wikipedia.org/wiki/Distance_(graph_theory))** possible, otherwise if two entries are hundreds of comparisons apart, how to reliably tell which one is better?
3. Nodes must have the **[same degree](https://en.wikipedia.org/wiki/Degree_(graph_theory))**. This is a fairness principle. Every entry should receive the same amount of attention: it would not be fair if an entry were compared only once while another entry had dozens of comparisons. So the graph must be **[regular](https://en.wikipedia.org/wiki/Regular_graph)**.
4. Constructing the graph should be easy to scale up with more and more contributions (arrows) while keeping these four properties true.

> We call such a graph a **bubble** since it is small and highly symmetric. And on a metaphorical level the competition itself is a small bubble around a shared interest.

This is somewhat similar to a [small world network](https://en.wikipedia.org/wiki/Small-world_network) because of the small diameter, but a key difference is that a small world network is [clustered](https://en.wikipedia.org/wiki/Clustering_coefficient) which is not what we want here. To be fair to all entries we want the graph to be regular. The popularity of an entry should emerge from the votes themselves, not the topology of the graph.

Since we are talking about a peer review process, these properties are realistic because the graph will have many times more arrows than nodes by asking competitors to each contribute a few comparisons.

### Ideal case

The best graph satisfying these properties is the **[complete graph](https://en.wikipedia.org/wiki/Complete_graph)** which has diameter 1 with all nodes connected.

A complete graph with N nodes has $\frac{N(N-1)}{2}$ arrows so in practice we cannot expect to build this graph, since each of the N competitors would have to rank about $\frac{N-1}{2}$ entries, which in practice is way too much.

The principles above allow us to relax the constraints of a complete graph while keeping nice properties. Indeed the following algorithm creates a graph with N nodes whose diameter is exponentially decreasing after each iteration.

## Bubbles

We can easily design a family of algorithms generating graphs with properties 1, 3 and 4 above. The idea is the following:

- Step 1: Connect all nodes in a cycle graph.
- Step k: Connect node i with node $F(N,k,i)$ for some function F of N (the size), k (the step) and i (the current node).

After step 1 all nodes have degree 2 and there are N arrows. The diameter is $\mathrm{floor}(\frac{N}{2})$.

After step k all nodes have degree $2k$ (F must be injective) and the graph has $kN$ arrows. The diameter at step k depends on the chosen function F, so we need to perform a benchmark to find the best function possible.

A simple family of such functions is $F(N,k,i) = i + f(N,k)$ for f based on usual functions like $\frac{N}{k}$ or $\frac{N}{2^k}$ etc. The video below shows the steps when $f(N,k) = \mathrm{ceil}(\frac{N}{2^k})$


https://user-images.githubusercontent.com/48696601/186481367-c9e00009-77ee-4439-a22a-63dd4cd15114.mp4


## Benchmark: generating the smallest bubble

When comparing two strategies F1 and F2 for building the graph, let's say F1 is **strongly** better than F2 if at **every** step of the algorithm, the diameter given by strategy F1 is less than or equal to the one given by strategy F2. Let's say it's **weakly** better if on average more steps are in favor of F1 than F2.

For the benchmark, we've looked at the first 10 iterations of the algorithm, on random samples of graphs of order between 100 and 10000.

The different strategies benchmarked are:
- Powers of two: based on $f(N,k)=\frac{N}{2^k}$
- Inverse: based on $f(N,k)=\frac{N}{1+k}$
- Square root: based on $f(N,k)=\frac{N}{1+\sqrt{k}}$
- Logarithm: based on $f(N,k)=\frac{N}{2+\log{k}}$
- Random:  choose a random integer between 2 and N//2 and use it for all pairings at step k. Make sure the function is injective so do not reuse integers.

You can run the benchmarks with `python -m scripts.benchmark`. See `benchmark.py` for the exact implementations.

### Example

This is the decrease in diameter for the different strategies when $n=4433$, showing an exponential decrease of the diameter in a log scale.


<p align="center">
  <img src="assets/benchmark.png" alt="benchmark" width="800">
</p>



After 4 steps with the v2 strategy, the graph has diameter 6.

### Results

When N is big enough there is a clear difference between the strategies:

- The inverse strategy is strongly better than the power of two strategy in 100% of samples
- The square root strategy is weakly better than the inverse strategy 82% of the time
- The log strategy is weakly better than the square root strategy 76% of the time
- The random strategy is almost always as good as the log strategy.

## Ranking

### Naive approach

A naive way to select the best nodes would be to pick the ones with the most wins.


https://user-images.githubusercontent.com/48696601/194752506-684f09a1-525d-4d52-aeeb-14a646df92fa.mp4


It's easier to win against a competitor who lost all his comparisons than it is to win against a competitor who wins most of his comparisons. So it's not enough to count the number of wins. We must take into account the relative strength of the losing nodes.


### PageRank

The situation is well suited for a [PageRank](https://en.wikipedia.org/wiki/PageRank) which is equivalent to flowing points in the graph. The idea is the following:

All nodes start with 1 point, so there are N points in the graph. This is a constant (the sum of all points) and points will flow in the graph: at each step, the points of a given node are divided among its outgoing arrows. So a node who lost 10 out of 10 comparisons will only contribute 0.1 points to each winner. This node tends to lose often so it's not so meaningful to win against it. On the contrary, a node that only lost one out of 10 comparisons will contribute one point to the winner. It means a lot more to win against this node.

We apply this procedure at least $\mathrm{diam}(G)$ times (the diameter of the graph) to allow the information to flow between any two nodes of the graph. The best nodes are the ones with the most points at the end of this procedure.


https://user-images.githubusercontent.com/48696601/194753795-f6d8412d-0606-4194-9da3-c4530739ee48.mp4

Notice at the end nodes D and E are equal with 0 points, but D should be better than E. Also if we ran the procedure one more time B would absorb A's point and all nodes but B (a sink) would have no points. To avoid these problems we use a [**damping factor**](https://en.wikipedia.org/wiki/PageRank#Damping_factor)


## License

[CC-BY-4.0](LICENSE)

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
