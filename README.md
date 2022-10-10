# NodeRank

Algorithm for massive competion judging. See the [contributing](#contributing) section.

## Description

In a big competition context, a few judges cannot rank all the entries, we need a **peer review** algorithm.

Also, assigning an absolute number to an entry is quite hard, and we often need to reevaluate the number after judging a few entries. It is far easier to estimate whether an entry is better than another entry. This is why the ranking will be based on **pairwise comparisons**, following other algorithms like [Gavel](https://www.anishathalye.com/2015/03/07/designing-a-better-judging-system/)

This way entries correspond quite naturally to the nodes of a directed graph where a comparison between two nodes is an arrow pointing to the better entry. The following algorithm describes how to construct this **comparison graph** and how to rank entries from this graph.

## Principles

We want the comparison graph to have the following properties:
1. It needs to be **connected**, since otherwise some islands of entries are not, even indirectly, comparable.
2. It needs to have the smallest **diameter** possible. Information quality decreases over long distances, so if two entries are hundreds of comparisons appart, how to reliably tell which one is better?
3. Nodes need to have the **same order**. This is a fairness principle. Every entry should receive the same amount of attention and have the same number of comparisons: it would not be fair if an entry were compared only once while another entry had dozens of comparisons.
4. Constructing the graph should be easy to scale up with more and more contributions (arrows) while keeping these four properties true.

Since we are talking about a peer review algorithm, these properties are realistic because the graph will have many times more arrows than nodes by asking competitors to each contribute a few comparisons.

### Ideal case

The best graph satisfying these properties is the **complete graph** which has diameter 1 with all nodes connected.

A complete graph with N nodes has $\frac{N(N-1)}{2}$ arrows so in practice we cannot expected to construct this graph, since each of the N competitors would need to rank about $\frac{N-1}{2}$ entries which in pratice is way too much.

So the principles above allow to relax the constaints of a complete graph, while keeping nice properties. Indeed the following algorithm creates a graph with N nodes whose diameter is exponentially decreasing after each iteration.

## Comparison graph

We can easily design a family of algorithms building graphs with properties 1, 3 and 4 above. The idea is the following:

- Step 1: connect all nodes in a cycle graph.
- Step k: connect node i with node $F(N,k,i)$ for some function F of N, k and i.

After step 1 all nodes have order 2 and there are N arrows. The diameter is $\mathrm{floor}(\frac{N}{2})$.

After step k all nodes have order $2k$ (F must be injective) and the graph has $kN$ arrows. The diameter at step k depends on the chosen function F, so we need to perform a benchmark to find the best function possible.

A simple family of such functions are $F(N,k,i) = i + f(N,k)$ for f based on usual functions like $\frac{N}{k}$ or $\frac{N}{2^k}$ etc. The video below shows the steps when $f(N,k) = \mathrm{ceil}(\frac{N}{2^k})$


https://user-images.githubusercontent.com/48696601/186481367-c9e00009-77ee-4439-a22a-63dd4cd15114.mp4



## Benchmark

When comparing two strategies F1 and F2 for building the comparison graph, let's say F1 is **strongly** better that F2 if at **every** step of the algorithm, the diameter given by strategy F1 is less than or equal to the one given by strategy F2. Let's say it's **weakly** better if on average more steps are in favor of F1 than F2.

For the benchmark we've looked at the first 10 iterations of the algorithm, on random samples of graphs of order between 100 and 10000.

The different stategies benchmarked are:
- Powers of two: based on $f(N,k)=\frac{N}{2^k}$
- Inverse: based on $f(N,k)=\frac{N}{1+k}$
- Square root: based on $f(N,k)=\frac{N}{1+\sqrt{k}}$
- Logarithm: based on $f(N,k)=\frac{N}{2+\log{k}}$

You can run the benchmarks with `python -m scripts.benchmark`. See `benchmark.py` for the exact implementations.

### Results

When N is big enough there is a clear difference between the strategies:

- The inverse strategy is strongly better than the power of two strategy in 100% of samples
- The square root strategy is weakly better than the inverse strategy 82% of the time
- The log strategy is weakly better than the square root strategy 76% of the time

### Example

This is the decrease in diameter for the different strategies when $n=4433$


<p align="center">
  <img src="assets/example.png" alt="benchmark" width="600">
</p>



After 8 steps with the log strategy the graph has diameter 6.

## Naive ranking

A naive way to select the best nodes would be to pick the ones with the most wins.


https://user-images.githubusercontent.com/48696601/194752506-684f09a1-525d-4d52-aeeb-14a646df92fa.mp4


It's easiser to win against a competitor who lost all his comparisons than it is to win against a competitor who wins most his comparisons. So it's not enough to count to number of wins. We must take into account the relative strength of the loosing nodes.


## NodeRank

All nodes start with 1 point, so there are N points in the graph. This is a constant (the sum of all points) but points will flow in the graph: at each step the points of a given node are divided among its outgoing arrows. So a node who lost 10 out of 10 comparisons will only contribute 0.1 point to each winner. This node tends to lose often so it's not so meaningul to win against it. On the contrary a node who only lost one out of 10 comparisons will contribute one point to the winner. It means a lot more to win against this node.

We apply this procedure $\mathrm{diam}(G)$ times (the diameter of the graph) to allow the information to flow between any two nodes of the graph. This way we get a more faithful representation of the value of nodes. The best ones are the ones with more points after $\mathrm{diam}(G)$ steps of this procedure.


https://user-images.githubusercontent.com/48696601/194753795-f6d8412d-0606-4194-9da3-c4530739ee48.mp4


### Complexity

- At step $k$ the judge i must compare nodes i and $i+f(N,k)$, so knowing what the next judge should do is $O(1)$.
- After $k$ steps the graph consists of $kN$ arrows and to compute the winners we need to flow points $\mathrm{diam}(G)$ times along these edges so the complexity of the ranking is $O(N)$


## Contributing

If you would like to make a suggestion, correct a typo or improve the algorithm/explanations/graphics, you're are welcome to send a pull request!

## License

[MIT](LICENSE)
