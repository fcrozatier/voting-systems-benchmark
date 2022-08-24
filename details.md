### Step 0

For the first iteration, randomly order the nodes in a list of size N and create a cycle graph from this list comparing nodes 0 and 1, nodes 1 and 2 etc. until nodes N-1 and 0.

<img src="assets/a.jpg" alt="Cycle with 10 nodes" width="400" style="display: block; margin-inline: auto;" >

After this step, each node has order 2, there are N arrows and the graph has diameter $\frac{N}{2}$. Some nodes win both of their comparisons, other win only one while other loose both.

Notice we can easily model the probabilities of the number of wins for a given node with a binomial distribution with parameters $n=2$ and $p=\frac{1}{2}$. This will nicely generalize in the next steps.

### Step 1

From now on, each step will roughly divide the diameter by a factor 2, while keeping the [4 properties](#principles) true.

The graph is symmetric and will stay symmetric so we can reason about its diameter by focusing on a single point. Pick node 0. Comparing it to node $\frac{N}{2}$ creates two cycles of diameter $\frac{N}{4}$. This node is now at distance at most $\frac{N}{4}$ of any other node.

<img src="assets/b.jpg" alt="Compare node 0 and node N/2" width="400" style="display: block; margin-inline: auto;">

Add a similar comparison for all nodes by comparing node $i$ and node $i+\frac{N}{2}$ and the resulting graph has diameter $\frac{N}{4}$. The exact value is $\mathrm{ceil}(\frac{N}{4})$.

<img src="assets/c.jpg" alt="Iteration 2" width="600" style="display: block; margin-inline: auto;">

This is the only step with two cases: compare nodes $i$ and $i + \frac{N}{2}$

- $N$ odd: no problem this adds $N$ arrows.
- $N$ even: arrows $(i, i + \frac{N}{2})$ and $(i + \frac{N}{2}, i + N)$ compare the same two points. We don't want to double the comparisons yet, it is more important to reduce the diameter of the graph. So this only adds $\frac{N}{2}$ arrows.


This step adds $\frac{N}{2}$ new arrows. At the end each node has order 3, and the number of wins of a given node follows the binomial distribution with parameters $n=3$ $p=\frac{1}{2}$

### Step 2

In step 2 node 0 was compared to node $\frac{N}{2}$ creating two cycles in which node 0 is at distance $\frac{N}{4}$ of any other node. Compare node 0 with node $\frac{N}{4}$. This divides the left cycle in two smaller cycles in which node 0 is at distance at most $\frac{N}{8}$ of any other nodes.

<img src="assets/d.jpg" alt="Compare node 0 with node N/4" width="400" style="display: block; margin-inline: auto;">

Add a similar comparison for all nodes by comparing node $i$ and node $i+\frac{N}{2}$. In particular comparing node $N-\frac{N}{4}$ with node 0 will take care of the right cycle mentionned just above. So node 0 is at distance at most $\frac{N}{8}$ of any other node. By symmetry the graph has diameter $\frac{N}{8}$.

This step adds $N$ new arrows. At the end each node has order 4, and the number of wins of a given node follows the binomial distribution with parameters $n=4$ $p=\frac{1}{2}$

### Step $k$

Continue in a similar fashion and compare nodes $i$ and $i+\frac{N}{2^k}$ for all $i$.

By the end of this step, the graph has $N$ new arrows.