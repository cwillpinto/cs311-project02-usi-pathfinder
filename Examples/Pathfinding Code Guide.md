# Pathfinding code explained

The lecture uses a schematic trip from BEC to Chick-fil-A (CF), via Liberal Arts (LA). Starbucks in Rice Library is SB; Arts Center is AC. Named destinations are familiar campus places; edge links/minute values are chosen for teaching. Starbucks and Chick-fil-A are not sponsors of these slides.

## Input and variable contracts

`graph` maps each place ID to `(neighbor, minutes)` pairs. Undirected edges appear both ways. Inputs use known string IDs and finite nonnegative weights. This small lecture function assumes valid inputs; it is not a full input validator. `start` is BEC, `goal` is CF. Each call creates its own best/parent/heap records.

`u` is the current popped place; `v` is one neighbor; `weight` is one edge's minutes. Dijkstra calls the actual accumulated cost `cost`; A* calls it `g`. `h` estimates what remains to the goal; `f=g+h` orders A* candidates. `best` stores g only. `parent` stores a predecessor ID, not a whole path.

## build_route

`def build_route(parent, goal):`

Receive the predecessor dictionary and destination ID; this helper returns only the ordered place list.

`route = []`

Create a fresh list; do not reuse or mutate an earlier returned route.

`current = goal`

Begin at CF because each predecessor points back toward BEC.

`while current is not None:`

Follow predecessors until the source sentinel None is reached. BEC itself is included.

`route.append(current)`

Save the current place: first CF, then LA, then BEC in this run.

`current = parent[current]`

Replace current with the place immediately before it; the search saved that link when a cost improved.

`route.reverse()`

The saved order is goal-to-source. Reverse the same list in place into BEC, LA, CF.

`return route`

Give the ordered list back to the calling search; reverse() itself would return None, so do not return route.reverse().

## dijkstra

`def dijkstra(graph, start, goal):`

Receive the adjacency dictionary and known source/destination IDs. Here start is BEC and goal is CF.

`best, parent = {start: 0}, {start: None}`

Create two fresh dictionaries per request. best stores the cheapest discovered actual cost g; parent stores one predecessor. The source costs zero and has no predecessor.

`heap = [(0, start)]`

Queue one (cost, place) candidate. One element is already a valid heap, so heapify is unnecessary.

`while heap:`

Continue while a candidate remains. Popping removes an entry; improvements can add entries. An empty frontier ends the search.

`cost, u = heapq.heappop(heap)`

Remove the smallest tuple and unpack it. cost is total start-to-u cost; u is the current place, for example LA. Equal costs compare the string IDs, so CF precedes SB.

`if cost != best[u]:`

Reject an obsolete candidate whose queued cost no longer equals the current best record. Improvements push a new entry rather than editing an old priority.

`continue`

Skip the remainder of this loop iteration and pop another candidate. This prevents an obsolete candidate from expanding neighbors or triggering an early goal return.

`if u == goal:`

Test whether the current, non-stale place is the destination. Nonnegative weights make this minimum-cost goal removal safe for Dijkstra.

`return build_route(parent, goal), cost`

Return a tuple (ordered path, actual cost). The helper follows parents; it does not recompute the cost.

`for v, weight in graph[u]:`

Iterate over u's adjacency list. Unpack each (neighbor ID, edge minutes) pair into v and weight. u stays fixed during this neighbor loop.

`new_cost = cost + weight`

Propose a route through u: full cost already traveled plus the single u-to-v edge. At LA, 4 + 3 proposes CF at 7.

`if new_cost < best.get(v, float("inf")):`

Look up the prior best cost for v. If unseen, use infinity as a comparison default without inserting it. Strict < accepts only improvements; equal routes retain the earlier parent.

`best[v], parent[v] = new_cost, u`

Remember both the improved total and the predecessor that achieves it. Keeping them together lets reconstruction agree with the reported cost.

`heapq.heappush(heap, (new_cost, v))`

Queue the improved offer and restore heap ordering. Older entries may remain; the stale check makes them harmless.

`return None, float("inf")`

This is after the while loop: the frontier ran out without reaching the goal. Return (None, infinity), not zero, because no route was found.

## a_star

`def a_star(graph, start, goal, h):`

Receive the same graph/source/goal and a dictionary of lower-bound remaining costs to this fixed goal. h uses minutes, not uncalibrated coordinate distance.

`best, parent = {start: 0}, {start: None}`

Create two fresh dictionaries per request. best stores the cheapest discovered actual cost g; parent stores one predecessor. The source costs zero and has no predecessor.

`heap = [(h[start], 0, start)]`

Queue (f, g, place). Since g at the source is zero, f = 0 + h[start]. At BEC this is (4, 0, BEC).

`while heap:`

Continue while a candidate remains. Popping removes an entry; improvements can add entries. An empty frontier ends the search.

`_, g, u = heapq.heappop(heap)`

Choose smallest f first, then g, then comparable place ID. _ is an ordinary variable name conventionally used for an unneeded value: it receives f. g and u are still needed.

`if g != best[u]:`

Compare actual queued g with actual best g. Comparing f against best[u] would mix estimated and actual costs and reject valid candidates.

`continue`

Skip the remainder of this loop iteration and pop another candidate. This prevents an obsolete candidate from expanding neighbors or triggering an early goal return.

`if u == goal:`

Test for a current goal after the stale check. A* needs the stated lower-bound heuristic, h(goal)=0 and correct improvement/reopening assumptions; nonnegative weights alone are not enough.

`return build_route(parent, goal), g`

Return actual travel cost g, not estimated priority f. At the goal the chosen h is zero, but the return contract should still explicitly use g.

`for v, weight in graph[u]:`

Iterate over u's adjacency list. Unpack each (neighbor ID, edge minutes) pair into v and weight. u stays fixed during this neighbor loop.

`new_g = g + weight`

Relax using actual traveled cost only. Do not add the heuristic to an edge weight or accumulate it into best.

`if new_g < best.get(v, float("inf")):`

Compare the new actual cost with the old actual cost, using infinity for an unseen neighbor.

`best[v], parent[v] = new_g, u`

Record the improved actual cost and predecessor exactly as in Dijkstra.

`entry = (new_g + h[v], new_g, v)`

Build the full candidate: first f = new_g + remaining estimate, then actual g, then ID. CF receives (7, 7, CF); SB receives (8, 7, SB).

`heapq.heappush(heap, entry)`

Queue the new priority. Requeue any genuine improvement, including one to a previously expanded place; no permanent closed set discards it.

`return None, float("inf")`

This is after the while loop: the frontier ran out without reaching the goal. Return (None, infinity), not zero, because no route was found.

## Why the stale check matters

If a candidate CF at cost 10 was queued and a later route improves best[CF] to 7, the old (10, CF) is obsolete. The cost-10 pop must not expand neighbors or return a goal. This illustrates a possible later state; the shown BEC-to-CF run returns at cost 7 before any such stale CF entry is popped.

## Assumptions behind an optimal result

Dijkstra needs nonnegative weights. A* uses lower-bound estimates, h(goal)=0, correct best-g comparisons and reopening when a cheaper route is found. The supplied estimates are also consistent on every edge. A* can visit fewer places here; that is not a guarantee on every graph. A one-element heap needs no heapify. Tuple ordering requires comparable place IDs or an explicit tie counter if using arbitrary objects.

## Returned values and project transfer

Both lecture functions return `(["BEC", "LA", "CF"], 7)`. Closing LA–CF in both directions in a copy of the lecture adjacency data gives BEC–LA–SB–CF at 9. Start equal to goal returns the one-place route and zero. A disconnected destination returns `(None, infinity)`.

The final project uses its original 10-waypoint campus_map_data.py and Graph-owned closures. Its return order is `(travel_time, path)`, or a single `None` when unreachable. Transfer the search method and adapt the interface; do not replace the supplied project data with this lecture graph. No project requirements or points change.

## Run

From the starter root: `python Examples/pathfinding_demo.py`. The main guard runs assertions and prints both results when executed directly; importing the module defines the functions/data without running those demonstration prints.

## Campus location sources

USI campus map: https://www.usi.edu/images/map/map.pdf

USI Fall 2026 dining: https://www.usi.edu/usitoday/announcements/2026/08/usi-dining-hours-for-2026-fall-semester

## Optional quad crossing

Earlier traces use the path-only graph. A second scenario copies its neighbor lists and adds BEC–CF in both directions at an illustrative weight of 6 minutes. With the quad available, both searches return `(["BEC", "CF"], 6)`, including when LA–CF is closed. Without the quad edge, the original route costs 7, or 9 when LA–CF is closed. Crossing drawn lines does not create a vertex. These times and access scenarios are hypothetical teaching inputs, not measured directions. Existing heuristic values remain lower bounds and consistent. Run the example to check all four scenarios. The graded project dataset is unchanged.
