# NodeRank+

Here I propose an algorithm for massive competion judging. See the [contributing](#contributing) section.

In a big competition context, a few judges cannot rank all the entries, so we need a **peer review** algorithm.

Also, assigning an absolute number to an entry is quite hard, and we often need to reevaluate the number after judging a few entries. It is far easier to estimate whether an entry is better than another entry. So the ranking will be based on **pairwise comparisons**, following other algorithms like [Gavel](https://www.anishathalye.com/2015/03/07/designing-a-better-judging-system/)

In this way entries correspond quite naturally to the nodes of a directed graph where a comparison between two nodes is an arrow pointing to the better entry. The algorithm needs to describe how to construct this **comparison graph** and how to rank entries from this graph.

## Principles

We want the comparison graph to have the following properties:
1. It needs to be **connected**, since otherwise some islands of entries are not, even indirectly, comparable.
2. It needs to have the smallest **diameter** possible. Information quality decreases over long distances, so if two entries are hundreds of comparisons appart, how to reliably tell which one is better?
3. Nodes need to have the **same order**. This is a fairness principle. Every entry should receive the same amount of attention and have the same number of comparisons: it would not be fair if an entry were compared only once while another entry had dozens of comparisons.
4. Constructing the graph should be easy to scale up with more and more contributions (arrows) while keeping these four properties true.

Since we are talking about a peer review algorithm, these properties are realistic because the graph will have many times more arrows than nodes by asking competitors to each contribute a few comparisons.

### Ideal case

The best graph satisfying these properties is the **complete graph** which has diameter 1 with all nodes connected.

A complete graph with $N$ nodes has $\frac{N(N-1)}{2}$ arrows so in practice we cannot expected to construct this graph, since each of the $N$ competitors would need to rank about $\frac{N-1}{2}$ entries which in pratice is too much.

So the principles above allow to relax the constaints of a complete graph, while keeping nice properties. Indeed the following algorithm creates a sequence of graphs with $N$ nodes that converges towards a complete graph after many iterations. The diameter is roughly divided by 2 after each iteration.

## Constructing the graph

Let say we have N nodes and assume this is a big number. The purpose of this discussion is a general explanation of the algorithm, specific details for when N is odd or even, or when $\frac{N}{2}$ is odd or even etc. are left to the implementation since they only marginally affect the general results.

### Step 1

For the first iteration, randomly order the nodes in a list of size N and create a cycle graph from this list comparing nodes 0 and 1, nodes 1 and 2 etc. until nodes N-1 and 0.

![Cycle with 10 nodes](assets/a.jpg)

After this step, each node has order 2, there are N arrows and the graph has diameter $\frac{N}{2}$. Some nodes win both of their comparisons, other win only one while other loose both.

Notice we can easily model the probabilities of the number of wins for a given node with a binomial distribution with parameters $n=2$ $p=\frac{1}{2}$. This will nicely generalize in the next steps.

### Step 2

From now on, each step will reduce the diameter by a factor 2, while keeping the [4 properties](#principles) true.

The graph is symmetric and will stay symmetric so we can reason about its diameter by focusing on a single point. Pick node 0. Comparing it to node $\frac{N}{2}$ creates two cycles of diameter $\frac{N}{4}$. This node is now at distance at most $\frac{N}{4}$ of any other node.

![Compare node 0 and node N/2](assets/b.jpg)

Add a similar comparison for all nodes by comparing node $i$ and node $i+\frac{N}{2}$ and the resulting graph has diameter $\frac{N}{4}$. The exact value is $\mathrm{ceil}(\frac{N}{4})$.


![Iteration 2](assets/c.jpg)

This step adds $\frac{N}{2}$ new arrows. At the end each node has order 3, and the number of wins of a given node follows the binomial distribution with parameters $n=3$ $p=\frac{1}{2}$

### Step 3

In step 2 node 0 was compared to node $\frac{N}{2}$ creating two cycles in which node 0 is at distance $\frac{N}{4}$ of any other node. Compare node 0 with node $\frac{N}{4}$. This divides the left cycle in two smaller cycles in which node 0 is at distance at most $\frac{N}{8}$ of any other nodes.

![Compare node 0 with node N/4](assets/d.jpg)

Add a similar comparison for all nodes by comparing node $i$ and node $i+\frac{N}{2}$. In particular comparing node $N-\frac{N}{4}$ with node 0 will take care of the right cycle mentionned just above. So node 0 is at distance at most $\frac{N}{8}$ of any other node. By symmetry the graph has diameter $\frac{N}{8}$.

This step adds $\frac{N}{2}$ new arrows. At the end each node has order 4, and the number of wins of a given node follows the binomial distribution with parameters $n=4$ $p=\frac{1}{2}$

### Step $k$

Continue in a similar fashion and compare nodes $i$ and $i+\frac{N}{2^{k-1}}$ for all $i$.

By the end of this step, the graph has $\frac{N}{2}$ new arrows, its diameter is $\frac{N}{2^k}$ and each node has order $k+1$.

## Example

If a competition has about ~1k competitors (let's say $2^{10}$ for convenience), and each competitor contributes 5 comparisons, then we can iterate the algorithm up to step 9 since each step after the first only needs half the competitors to complete.

This mean the comparison graph has diameter $\frac{2^{10}}{2^9}=2$ so it's almost a **complete graph**

## Naive ranking

A naive way to select the best nodes would be to pick the ones with the most wins.

Following the previous example, after step 9 each node has order 10 and the probability for a given node to win 9 or 10 over 10 comparisons is, using a binomial distribution with parameters $n=10$ $p=\frac{1}{2}$:

$$
\frac{1}{2^{10}}\left(\binom{10}{9}+\binom{10}{10}\right)=\frac{11}{2^{10}}
$$

So in a competition with $2^{10}$ competitors this would select about 11 entries.

But it's easiser to win against a competitor who lost all his comparisons that to win against a competitor who wins most his comparisons. So it's not enough to count to number of wins. We must take into account the relative strength of the loosing nodes.


## NodeRank

All nodes start with 1 point, so there are $N$ points in the graph. This is a constant (the sum of all points) but points will flow in the graph: at each step the points of a given node are divided among its outgoing arrows. So a node who lost 10 out of 10 comparisons will only contribute 0.1 point to each winner. This node tends to lose often so it's not so meaningul to win against it. On the contrary a node who only lost one out of 10 comparisons will contribute one point to the winner. It means a lot more to win against this node.

We apply this procedure $\mathrm{diam}(G)$ times (the diameter of the graph) to allow the information to flow between any two nodes of the graph. This way we get a more faithful representation of the value of nodes. The best ones are the ones with more points after $\mathrm{diam}(G)$ steps of this procedure.

The name is inpired from the PageRank algorithm. But there is more in the next section. As-is this algorithm promotes nodes with many wins against nodes with many wins themselves. But couldn't it be that a node only happened to be compared to weaker entries, while still being a very good entry ? This kind of node would be stuck with only a few points while still being a very good entry.

It would be nice to avoid this situation by design while keeping the other properties.

### Complexity

- At step $k$ the judge $i$ must compare nodes $i$ and $i+\frac{N}{2^{k-1}}$, so knowing what the next judge should do is $O(1)$.
- After $k$ steps the graph consists of $N+(k-1)\frac{N}{2}$ arrows and to compute the winners we need to flow points $\mathrm{diam}(G)$ times along these edges so the complexity is $O(Nk)$

## NodeRank+

Coming soon!


## Contributing

If you would like to make a suggestion, correct a typo or improve the algorithm/explanation/graphics, you can send a pull request, they are welcome !