# Near-BEC pathfinding lecture example. Links/weights are illustrative, not actual directions.
# BEC: Business & Engineering; LA: Liberal Arts; AC: Arts Center.
# SB: Starbucks in Rice Library; CF: Chick-fil-A in UC West.
# Starbucks and Chick-fil-A are not sponsors of these slides or this example.
# Receive the predecessor dictionary and destination ID; this helper returns only the ordered place list.
def build_route(parent, goal):
    # Create a fresh list; do not reuse or mutate an earlier returned route.
    route = []
    # Begin at CF because each predecessor points back toward BEC.
    current = goal
    # Follow predecessors until the source sentinel None is reached. BEC itself is included.
    while current is not None:
        # Save the current place: first CF, then LA, then BEC in this run.
        route.append(current)
        # Replace current with the place immediately before it; the search saved that link when a cost improved.
        current = parent[current]
    # The saved order is goal-to-source. Reverse the same list in place into BEC, LA, CF.
    route.reverse()
    # Give the ordered list back to the calling search; reverse() itself would return None, so do not return route.reverse().
    return route

# Import Python min-heap operations. A heap exposes the smallest candidate without scanning the entire list.
import heapq

# Receive the adjacency dictionary and known source/destination IDs. Here start is BEC and goal is CF.
def dijkstra(graph, start, goal):
    # Create two fresh dictionaries per request. best stores the cheapest discovered actual cost g; parent stores one predecessor. The source costs zero and has no predecessor.
    best, parent = {start: 0}, {start: None}
    # Queue one (cost, place) candidate. One element is already a valid heap, so heapify is unnecessary.
    heap = [(0, start)]
    # Continue while a candidate remains. Popping removes an entry; improvements can add entries. An empty frontier ends the search.
    while heap:
        # Remove the smallest tuple and unpack it. cost is total start-to-u cost; u is the current place, for example LA. Equal costs compare the string IDs, so CF precedes SB.
        cost, u = heapq.heappop(heap)
        # Reject an obsolete candidate whose queued cost no longer equals the current best record. Improvements push a new entry rather than editing an old priority.
        if cost != best[u]:
            # Skip the remainder of this loop iteration and pop another candidate. This prevents an obsolete candidate from expanding neighbors or triggering an early goal return.
            continue
        # Test whether the current, non-stale place is the destination. Nonnegative weights make this minimum-cost goal removal safe for Dijkstra.
        if u == goal:
            # Return a tuple (ordered path, actual cost). The helper follows parents; it does not recompute the cost.
            return build_route(parent, goal), cost
        # Iterate over u's adjacency list. Unpack each (neighbor ID, edge minutes) pair into v and weight. u stays fixed during this neighbor loop.
        for v, weight in graph[u]:
            # Propose a route through u: full cost already traveled plus the single u-to-v edge. At LA, 4 + 3 proposes CF at 7.
            new_cost = cost + weight
            # Look up the prior best cost for v. If unseen, use infinity as a comparison default without inserting it. Strict < accepts only improvements; equal routes retain the earlier parent.
            if new_cost < best.get(v, float("inf")):
                # Remember both the improved total and the predecessor that achieves it. Keeping them together lets reconstruction agree with the reported cost.
                best[v], parent[v] = new_cost, u
                # Queue the improved offer and restore heap ordering. Older entries may remain; the stale check makes them harmless.
                heapq.heappush(heap, (new_cost, v))
    # This is after the while loop: the frontier ran out without reaching the goal. Return (None, infinity), not zero, because no route was found.
    return None, float("inf")

# Receive the same graph/source/goal and a dictionary of lower-bound remaining costs to this fixed goal. h uses minutes, not uncalibrated coordinate distance.
def a_star(graph, start, goal, h):
    # Create two fresh dictionaries per request. best stores the cheapest discovered actual cost g; parent stores one predecessor. The source costs zero and has no predecessor.
    best, parent = {start: 0}, {start: None}
    # Queue (f, g, place). Since g at the source is zero, f = 0 + h[start]. At BEC this is (4, 0, BEC).
    heap = [(h[start], 0, start)]
    # Continue while a candidate remains. Popping removes an entry; improvements can add entries. An empty frontier ends the search.
    while heap:
        # Choose smallest f first, then g, then comparable place ID. _ is an ordinary variable name conventionally used for an unneeded value: it receives f. g and u are still needed.
        _, g, u = heapq.heappop(heap)
        # Compare actual queued g with actual best g. Comparing f against best[u] would mix estimated and actual costs and reject valid candidates.
        if g != best[u]:
            # Skip the remainder of this loop iteration and pop another candidate. This prevents an obsolete candidate from expanding neighbors or triggering an early goal return.
            continue
        # Test for a current goal after the stale check. A* needs the stated lower-bound heuristic, h(goal)=0 and correct improvement/reopening assumptions; nonnegative weights alone are not enough.
        if u == goal:
            # Return actual travel cost g, not estimated priority f. At the goal the chosen h is zero, but the return contract should still explicitly use g.
            return build_route(parent, goal), g
        # Iterate over u's adjacency list. Unpack each (neighbor ID, edge minutes) pair into v and weight. u stays fixed during this neighbor loop.
        for v, weight in graph[u]:
            # Relax using actual traveled cost only. Do not add the heuristic to an edge weight or accumulate it into best.
            new_g = g + weight
            # Compare the new actual cost with the old actual cost, using infinity for an unseen neighbor.
            if new_g < best.get(v, float("inf")):
                # Record the improved actual cost and predecessor exactly as in Dijkstra.
                best[v], parent[v] = new_g, u
                # Build the full candidate: first f = new_g + remaining estimate, then actual g, then ID. CF receives (7, 7, CF); SB receives (8, 7, SB).
                entry = (new_g + h[v], new_g, v)
                # Queue the new priority. Requeue any genuine improvement, including one to a previously expanded place; no permanent closed set discards it.
                heapq.heappush(heap, entry)
    # This is after the while loop: the frontier ran out without reaching the goal. Return (None, infinity), not zero, because no route was found.
    return None, float("inf")

graph = {'BEC': [('LA', 4), ('AC', 5)], 'LA': [('BEC', 4), ('SB', 3), ('CF', 3), ('AC', 3)], 'SB': [('LA', 3), ('CF', 2)], 'CF': [('LA', 3), ('SB', 2)], 'AC': [('BEC', 5), ('LA', 3)]}

estimates = {'BEC': 4, 'LA': 2, 'AC': 3, 'SB': 1, 'CF': 0}

if __name__ == "__main__":
    expected = (["BEC", "LA", "CF"], 7)
    result_d = dijkstra(graph, "BEC", "CF")
    result_a = a_star(graph, "BEC", "CF", estimates)
    assert result_d == result_a == expected
    print("Dijkstra:", result_d)
    print("A*:", result_a)

    # A second model permits a direct crossing of the quad.
    # Six minutes is an illustrative teaching weight, not a measured time.
    quad = {place: list(neighbors) for place, neighbors in graph.items()}
    quad["BEC"].append(("CF", 6))
    quad["CF"].append(("BEC", 6))
    expected_quad = (["BEC", "CF"], 6)
    assert dijkstra(quad, "BEC", "CF") == expected_quad
    assert a_star(quad, "BEC", "CF", estimates) == expected_quad
    print("Quad open (both algorithms):", expected_quad)

    # Keep the quad and path closure choices independent.
    for name, model, expected_result in [
        ("Paths only; LA-CF closed", graph, (["BEC", "LA", "SB", "CF"], 9)),
        ("Quad open; LA-CF closed", quad, expected_quad),
    ]:
        closed = {
            place: [(neighbor, weight) for neighbor, weight in neighbors
                    if {place, neighbor} != {"LA", "CF"}]
            for place, neighbors in model.items()
        }
        assert dijkstra(closed, "BEC", "CF") == expected_result
        assert a_star(closed, "BEC", "CF", estimates) == expected_result
        print(name + " (both algorithms):", expected_result)
