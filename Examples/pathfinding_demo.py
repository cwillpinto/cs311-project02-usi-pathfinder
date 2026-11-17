# Class example: BEC, Liberal Arts (LA), Arts Center (AC),
# Starbucks at Rice Library (SB), and Chick-fil-A at UC West (CF).
# Connections and times are made up for the lesson.
# Read Pathfinding Code Guide.md for the line-by-line explanation.

import heapq


def build_route(parent, goal):
    route = []
    # Work backward from the destination, then reverse the path.
    current = goal
    while current is not None:
        route.append(current)
        current = parent[current]
    route.reverse()
    return route


def dijkstra(graph, start, goal):
    best, parent = {start: 0}, {start: None}
    heap = [(0, start)]
    while heap:
        cost, u = heapq.heappop(heap)
        # A cheaper entry may have been queued since this one was added.
        if cost != best[u]:
            continue
        if u == goal:
            return build_route(parent, goal), cost
        for v, weight in graph[u]:
            new_cost = cost + weight
            # Keep the earlier parent when two routes have the same cost.
            if new_cost < best.get(v, float("inf")):
                best[v], parent[v] = new_cost, u
                heapq.heappush(heap, (new_cost, v))
    return None, float("inf")


def a_star(graph, start, goal, h):
    best, parent = {start: 0}, {start: None}
    heap = [(h[start], 0, start)]
    while heap:
        # The heap orders by f; use g to check the actual route cost.
        _, g, u = heapq.heappop(heap)
        if g != best[u]:
            continue
        if u == goal:
            return build_route(parent, goal), g
        for v, weight in graph[u]:
            new_g = g + weight
            if new_g < best.get(v, float("inf")):
                best[v], parent[v] = new_g, u
                # Queue f, g, and the place ID, in that order.
                entry = (new_g + h[v], new_g, v)
                heapq.heappush(heap, entry)
    return None, float("inf")

graph = {
    'BEC': [('LA', 4), ('AC', 5)],
    'LA': [('BEC', 4), ('SB', 3), ('CF', 3), ('AC', 3)],
    'SB': [('LA', 3), ('CF', 2)],
    'CF': [('LA', 3), ('SB', 2)],
    'AC': [('BEC', 5), ('LA', 3)],
}

estimates = {'BEC': 4, 'LA': 2, 'AC': 3, 'SB': 1, 'CF': 0}

if __name__ == "__main__":
    expected = (["BEC", "LA", "CF"], 7)
    result_d = dijkstra(graph, "BEC", "CF")
    result_a = a_star(graph, "BEC", "CF", estimates)
    assert result_d == result_a == expected
    print("Dijkstra:", result_d)
    print("A*:", result_a)

    # Copy the neighbor lists so the original map stays unchanged.
    quad = {place: list(neighbors) for place, neighbors in graph.items()}
    # Six minutes is a teaching value, not a measured walking time.
    quad["BEC"].append(("CF", 6))
    quad["CF"].append(("BEC", 6))
    expected_quad = (["BEC", "CF"], 6)
    assert dijkstra(quad, "BEC", "CF") == expected_quad
    assert a_star(quad, "BEC", "CF", estimates) == expected_quad
    print("Quad open (both algorithms):", expected_quad)

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
