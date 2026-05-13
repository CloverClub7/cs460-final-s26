"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Owen Zhang
Student ID:   131832646

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.
    """

    part_1 = '''Why a single shortest-path run from S is not enough:\n
                Since there are multiple targets we must visit before we can go to the exit node, a single shortest-path run will not yield the best route from S to all targets then to T.\n
                We would need to plan and note several routes from S to the multiple targets, from each target to every other target, and from every target to T, or the inter-location costs.\n
                \n
                What decision remains after all inter-location costs are known:\n
                Decide which permutation of the order of relic nodes visited uses the least fuel.\n
                \n
                Why this requires a search over orders:\n
                Every permutation of relic nodes must be considered and greedy by itself can't work since choosing the best node at one instance might create a longer overall path.'''
    return part_1


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.
    """

    sources = [spawn]
    # Assumes that relic list does not have duplicates
    # If so we can convert to set then back to list... but ion wanna for now
    sources = sources + relics
    return sources


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').
    """
    
    priority_queue = []
    costs = {}

    # Make costs dictionary with every node in graph
    for node in graph:
        costs[node] = float('inf')

    costs[source] = 0
    heapq.heappush(priority_queue, (0, source))

    # Process from source node to every other reachable node
    while priority_queue:
        cost, current_node = heapq.heappop(priority_queue)

        # Skip of cost is already more than already computed
        if cost > costs[current_node]:
            continue

        # Visit all reachable nodes from source
        for destination_node, destination_cost in graph[current_node]:
            new_cost = costs[current_node] + destination_cost

            # Update if path of less cost is found
            if new_cost < costs[destination_node]:
                costs[destination_node] = new_cost
                heapq.heappush(priority_queue, (costs[destination_node], destination_node))

    return costs


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.
    """
    distances_table = {}
    sources = select_sources(spawn, relics, exit_node)

    # Run Dijkstra's for every source
    for source in sources:
        distances = run_dijkstra(graph, source)
        distances_table[source] = distances

    return distances_table



# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    """
    part_3 = '''Part 3a: What the Invariant Means\n
                For nodes already finalized (in S):\n
                Finalised nodes in S have the shortest path from the source calculated.\n
                \n
                For nodes not yet finalized (not in S):\n
                Nodes not yet in S do not yet have the shortest distance from the source found, they may have longer distances stored.\n
                \n
                Part 3b: Why Each Phase Holds\n
                \n
                Initialization : why the invariant holds before iteration 1:\n
                Before the first step, the source node is finalised with 0 in S.\n
                This is correct as the cost from a node to itself is 0.\n
                \n
                Maintenance : why finalizing the min-dist node is always correct:\n
                The min-dist node will have the smallest cost needed to reach it and other unfinalised nodes already cost as much or more than the min-dist node.\n
                Since edge weights are nonnegative, other paths that go through another unfinalised node will have that weight added onto the total, producing a larger cost.\n
                \n
                Termination : what the invariant guarantees when the algorithm ends:\n
                That for every node in S, the cost is the true shortest-path distance from the source to the node.\n
                \n
                Part 3c: Why This Matters for the Route Planner\n
                \n
                The routing decision chooses the shortest route based on the path distances, so distances need to be correct in order to find a valid and optimal ordering of routes.'''
    return part_3


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.

    """
    part_4 = '''The failure mode: The least-cost route is not found.\n
                Counter-example setup: Let the following table contain the cheapest inter-location travel costs.\n
                \n
                | From \ To | B   | C   | D   | T   |\n
                |-----------|-----|-----|-----|-----|\n
                | S         | 1   | 2   | 2   | --  |\n
                | B         | --  | 100 | 100 | 1   |\n
                | C         | 1   | --  | 100 | 1   |\n
                | D         | 1   | 1   | --  | 100 |\n
                \n
                What greedy picks: [B, C, D, T], total: 1 + 100 + 100 + 100 = 301\n
                What optimal picks: [D, C, B, T], total: 2 + 1 + 1 + 1 = 5\n
                Why greedy loses: By choosing the best local option, it is barred from the best global route (better future choice).\n
                \n
                What the Algorithm Must Explore\n
                Different orders of nodes (inter-location routes) and find the least-cost permutation.'''
    
    return part_4


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    """
    final_route = [float('inf'), []]
    relics_remaining = set(relics)

    _explore(dist_table, spawn, relics_remaining, [], 0, exit_node, final_route)
    return final_route[0], final_route[1]


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.

    TODO
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
    if not relics_remaining:
        total_cost = cost_so_far + dist_table[current_loc][exit_node]
        if total_cost < best[0]:
            best[0] = total_cost
            best[1] = relics_visited_order + [exit_node]
        return

    # If the cost so far is already greater than the currently stored cost, 
    # there is no way for this route to be less than the current best. Also 
    # catches if no valid routes exist (float('inf') >= float('inf') = true).
    if cost_so_far >= best[0]:
        return

    for relic in relics_remaining:
        # Update
        cost_so_far += dist_table[current_loc][relic]
        relics_remaining.remove(relic)
        relics_visited_order.append(relic)
        
        # Recurse
        _explore(dist_table, relic, relics_remaining, relics_visited_order,
                 cost_so_far, exit_node, best)
        
        # Backtrack
        cost_so_far -= dist_table[current_loc][relic]
        relics_remaining.add(relic)
        relics_visited_order.pop()


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.
    """
    
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    route_tuple = find_optimal_route(dist_table, spawn, relics, exit_node)
    return route_tuple


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
