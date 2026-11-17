# Pathfinding code explained

The lecture uses a schematic trip from BEC to Chick-fil-A (CF), via Liberal Arts (LA). Starbucks in Rice Library is SB; Arts Center is AC. The places are real; the connections and travel times are made up for class.

## Inputs and variable names

`graph` maps each place ID to `(neighbor, minutes)` pairs. Undirected edges appear both ways. Inputs use known string IDs and finite nonnegative weights. This small lecture function assumes valid inputs; it is not a full input validator. `start` is BEC, `goal` is CF. Each call creates its own best/parent/heap records.

`u` is the current popped place; `v` is one neighbor; `weight` is one edge's minutes. Dijkstra calls the actual accumulated cost `cost`; A* calls it `g`. `h` estimates what remains to the goal; `f=g+h` orders A* candidates. `best` stores g only. `parent` stores a predecessor ID, not a whole path.

## build_route

`def build_route(parent, goal):`

Use `parent` to build the list of places from the start to `goal`.

`route = []`

Start a new list for this route.

`current = goal`

Start at the destination, CF, and follow the parents back toward BEC.

`while current is not None:`

Keep going until `current` reaches `None`, the parent of BEC.

`route.append(current)`

Add the current place to the route. Here the order is CF, LA, BEC.

`current = parent[current]`

Move to the previous place stored in `parent`.

`route.reverse()`

Reverse the list to get BEC, LA, CF.

`return route`

Return the finished list. Call `reverse()` first; it changes the list and returns `None`.

## dijkstra

`def dijkstra(graph, start, goal):`

Take the graph, starting place, and destination as arguments.

`best, parent = {start: 0}, {start: None}`

Start fresh for each request: `best` stores costs and `parent` stores predecessors. The start costs zero and has no predecessor.

`heap = [(0, start)]`

Put `(0, start)` in the heap. A list with one entry needs no `heapify()` call.

`while heap:`

Keep searching while the heap has entries.

`cost, u = heapq.heappop(heap)`

Pop the cheapest entry into `cost` and `u`. Equal costs are ordered by the string IDs, so CF comes before SB.

`if cost != best[u]:`

Skip this entry if a cheaper cost for `u` has been saved since it was queued.

`continue`

Skip the remaining lines in this iteration and go back to the heap.

`if u == goal:`

If this current entry is the goal, Dijkstra has found a cheapest route because the weights are nonnegative.

`return build_route(parent, goal), cost`

Build the path from the parents and return it with the cost.

`for v, weight in graph[u]:`

Visit each neighbor `v` of `u`; `weight` is the cost of that edge.

`new_cost = cost + weight`

Add the edge cost to the cost so far. From LA to CF, this is 4 + 3 = 7.

`if new_cost < best.get(v, float("inf")):`

Use infinity if `v` has not been reached. Update only for a cheaper route; an equal cost keeps the earlier parent.

`best[v], parent[v] = new_cost, u`

Save the improved cost and the parent that gave that cost.

`heapq.heappush(heap, (new_cost, v))`

Push the improved entry. The stale check will skip older entries later.

`return None, float("inf")`

If the heap empties without reaching the goal, return `(None, infinity)`.

## a_star

`def a_star(graph, start, goal, h):`

Use the same inputs as Dijkstra, plus `h`, a dictionary of lower-bound estimates in minutes.

`best, parent = {start: 0}, {start: None}`

Start fresh for each request: `best` stores costs and `parent` stores predecessors. The start costs zero and has no predecessor.

`heap = [(h[start], 0, start)]`

Queue `(f, g, place)`. At BEC, `g=0` and `h=4`, so the first entry is `(4, 0, BEC)`.

`while heap:`

Keep searching while the heap has entries.

`_, g, u = heapq.heappop(heap)`

Pop the smallest `f`, breaking ties by `g` and place ID. `_` receives `f`, which this line no longer needs.

`if g != best[u]:`

Compare `g` with `best[u]`. Both are actual costs; `f` also includes an estimate.

`continue`

Skip the remaining lines in this iteration and go back to the heap.

`if u == goal:`

Check for the goal after skipping stale entries. This A* version uses lower-bound estimates, `h[goal]=0`, and permits later improvements.

`return build_route(parent, goal), g`

Return the path and its actual cost `g`.

`for v, weight in graph[u]:`

Visit each neighbor `v` of `u`; `weight` is the cost of that edge.

`new_g = g + weight`

Add the edge weight to `g`. Keep the estimate out of the actual cost.

`if new_g < best.get(v, float("inf")):`

Check whether `new_g` improves the saved cost, using infinity for an unseen neighbor.

`best[v], parent[v] = new_g, u`

Save the improved cost and parent, as in Dijkstra.

`entry = (new_g + h[v], new_g, v)`

Queue `f`, `g`, and the place ID. CF gets `(7, 7, CF)`; SB gets `(8, 7, SB)`.

`heapq.heappush(heap, entry)`

Push the new entry, even if the place was expanded earlier. A cheaper route must still be considered.

`return None, float("inf")`

If the heap empties without reaching the goal, return `(None, infinity)`.

## Why the stale check matters

If a candidate CF at cost 10 was queued and a later route improves best[CF] to 7, the old (10, CF) is obsolete. The cost-10 pop must not expand neighbors or return a goal. This illustrates a possible later state; the shown BEC-to-CF run returns at cost 7 before any such stale CF entry is popped.

## Assumptions behind an optimal result

Dijkstra needs nonnegative weights. A* uses lower-bound estimates, h(goal)=0, correct best-g comparisons and reopening when a cheaper route is found. The supplied estimates are also consistent on every edge. A* can visit fewer places here; that is not a guarantee on every graph. A one-element heap needs no heapify. Tuple ordering requires comparable place IDs or an explicit tie counter if using arbitrary objects.

## Returned values and project transfer

Both lecture functions return `(["BEC", "LA", "CF"], 7)`. Closing LA–CF in both directions in a copy of the lecture adjacency data gives BEC–LA–SB–CF at 9. Start equal to goal returns the one-place route and zero. A disconnected destination returns `(None, infinity)`.

The final project uses its original 10-waypoint campus_map_data.py and Graph-owned closures. Its return order is `(travel_time, path)`, or a single `None` when unreachable. Transfer the search method and adapt the interface; do not replace the supplied project data with this lecture graph. No project requirements or points change.

## Run

From the starter root: `python Examples/pathfinding_demo.py`. Running the file checks the examples and prints the results. Importing it does not run those examples.

## Campus location sources

USI campus map: https://www.usi.edu/images/map/map.pdf

USI Fall 2026 dining: https://www.usi.edu/usitoday/announcements/2026/08/usi-dining-hours-for-2026-fall-semester

## Optional quad crossing

Earlier traces use the path-only graph. A second scenario copies its neighbor lists and adds BEC–CF in both directions at an illustrative weight of 6 minutes. With the quad available, both searches return `(["BEC", "CF"], 6)`, including when LA–CF is closed. Without the quad edge, the original route costs 7, or 9 when LA–CF is closed. Crossing drawn lines does not create a vertex. These times and access scenarios are hypothetical teaching inputs, not measured directions. Existing heuristic values remain lower bounds and consistent. Run the example to check all four scenarios. The graded project dataset is unchanged.
