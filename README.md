# The Torchbearer

**Student Name:** Owen Zhang
**Student ID:** 131832646
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  - Since there are multiple targets we must visit before we can go to the exit node, a single 
    shortest-path run will not yield the best route from S to all targets then to T. 
  - We would need to plan and note several routes from S to the multiple targets, from each 
    target to every other target, and from every target to T, or the inter-location costs.

- **What decision remains after all inter-location costs are known:**
  - Decide which permutation of the order of relic nodes visited uses the least fuel. 

- **Why this requires a search over orders (one sentence):**
  - Every permutation of relic nodes must be considered and greedy by itself can't work since 
    choosing the best node at one instance might create a longer overall path.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source |
|---|---|
| Starting Node | Path must be computed starting from here, so one inter-location cost starting from S must be chosen. |
| Relic Node | Path must visit all relic nodes, so one inter-location cost from each relic nodes must be chosen. |

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property | Your answer |
|---|---|
| Data structure name | Dictionary |
| What the keys represent | Source Node |
| What the values represent | Table of pre-computed least costs to get to every other node, excluding S |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | Dictionaries use hashing with keys to acheive O(1) lookups |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** n + 1, where n is the number of relic nodes. Plus 1 for S.
- **Cost per run:** O((V + E)log V)
- **Total complexity:** O(n(V + E)log V)
- **Justification (one line):** O((V + E)log V) cost is ran n + 1 times, 1 is dropped per big-O.

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  - Finalised nodes in S have the shortest path from the source calculated.

- **For nodes not yet finalized (not in S):**
  - Nodes not yet in S do not yet have the shortest distance from the source found, they may have longer distances stored.

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  - Before the first step, the source node is finalised with 0 in S.
  - This is correct as the cost from a node to itself is 0.

- **Maintenance : why finalizing the min-dist node is always correct:**
  - The min-dist node will have the smallest cost needed to reach it and other unfinalised nodes already cost as much or 
    more than the min-dist node.
  - Since edge weights are nonnegative, other paths that go through another unfinalised node will have that weight 
    added onto the total, producing a larger cost.

- **Termination : what the invariant guarantees when the algorithm ends:**
  - That for every node in S, the cost is the true shortest-path distance from the source to the node.

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

The routing decision chooses the shortest route based on the path distances, so distances need to be correct in order to 
find a valid and optimal ordering of routes.

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** The least-cost route is not found.
- **Counter-example setup:** Let the following table contain the cheapest inter-location travel costs.

  | From \ To | B   | C   | D   | T   |
  |-----------|-----|-----|-----|-----|
  | S         | 1   | 2   | 2   | --  |
  | B         | --  | 100 | 100 | 1   |
  | C         | 1   | --  | 100 | 1   |
  | D         | 1   | 1   | --  | 100 |

- **What greedy picks:** [B, C, D, T], total: 1 + 100 + 100 + 100 = 301
- **What optimal picks:** [D, C, B, T], total: 2 + 1 + 1 + 1 = 5
- **Why greedy loses:** By choosing the best local option, it is barred from the best global route (better future choice).

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- Different orders of nodes (inter-location routes) and find the least-cost permutation.

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_loc | string | Current node the algorithm is at. |
| Relics already collected | relics_remaining | set | Relic nodes that still need to be visited. |
| Fuel cost so far | cost_so_far | int | The cost so far of the current run. |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | set |
| Operation: check if relic already collected | Time complexity: O(1) |
| Operation: mark a relic as collected | Time complexity: O(1) |
| Operation: unmark a relic (backtrack) | Time complexity: O(1) |
| Why this structure fits | No inherent need for an order since all nodes need to be visited. O(1) complexity for needed operations. |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** k!, where k is the number of relic nodes.
- **Why:** In the worst-case, all orderings of k nodes need to be considered which is k! orderings.

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** cost_so_far
- **When it is used:** to compare to the best cost at every recursion.
- **What it allows the algorithm to skip:** skips routes that are guaranteed to cost more than what is stored in best.

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** the tenative cost of the current run and the best cost we've had so far.
- **What the lower bound accounts for:** cost to the nearest unvisited relic node and the minimum cost from all remaining relic nodes to the exit node.
- **Why it never overestimates:** choosing minimum costs nets us minamal total cost that doesn't exceed the actual remaining cost.

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- If the cost so far is already greater than the currently stored cost, 
  there is no way for this route to be less than the current best.
- Moreover, nonnegative weights means that any future legs added to the route 
  will always increase the total cost.
---

## References

> Bullet list. If none beyond lecture notes, write that.

- Lecture notes
- Python Sets: What, Why and How (https://labex.io/pythoncheatsheet/blog/python-sets-what-why-how)
