# Development Log – The Torchbearer

**Student Name:** Owen Zhang
**Student ID:** 131832646

> Instructions: Write at least four dated entries. Required entry types are marked below.
> Two to five sentences per entry is sufficient. Write entries as you go, not all in one
> sitting. Graders check that entries reflect genuine work across multiple sessions.
> Delete all blockquotes before submitting.

---

## Entry 1 – [05.07.2026]: Initial Plan

> Required. Write this before writing any code. Describe your plan: what you will
> implement first, what parts you expect to be difficult, and how you plan to test.

I think I will implement this step-by-step, as this way will probably be the least 
confusing. So we'll get the values, compute distances, then sort and find the best 
possible path. I expect properly understanding the problem to be most difficult, 
but after that I think I can pull through. I can see computing the shortest path 
from each node and the logic of finding the best path as definite challenges. As 
of now I plan to test with the test functions at the end of the file, maybe fill
in my own values as well.

---

## Entry 2 – [05.08.2026]: [Short description]

> Required. At least one entry must describe a bug, wrong assumption, or design change
> you encountered. Describe what went wrong and how you resolved it.

Implemented the Djikstra part to find shortest runs for all nodes to all other nodes. 
This part seemed pretty straightforward, so deciding which run is the best might 
be the real challenge.

---

## Entry 3 – [05.12.2026]: [Short description]

During part 3, I assumed that S had the results of all nodes (after all Dijkstra 
instances were run) rather than just the results for the current node. After fixing 
this assumption, finishing the part became much easier.

---

## Entry 4 – [05.12.2026]: Post-Implementation Reflection

> Required. Written after your implementation is complete. Describe what you would
> change or improve given more time.

Not sure what I would change even if given more time. I noticed that the total 
complexity of the algorithm isn't great, with the route decision part possibly taking 
O(k!) time. Djikstra's is Djikstra's so I think if there are any improvements to be 
made it'll be in the decision part.

---

## Final Entry – [05.12.2026]: Time Estimate

> Required. Estimate minutes spent per part. Honesty is expected; accuracy is not graded.

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 1 |
| Part 2: Precomputation Design | 1 |
| Part 3: Algorithm Correctness | 1 |
| Part 4: Search Design | 0.5 |
| Part 5: State and Search Space | 2 |
| Part 6: Pruning | 0.5 |
| Part 7: Implementation | 2 |
| README and DEVLOG writing | 1 |
| **Total** | 9 |
