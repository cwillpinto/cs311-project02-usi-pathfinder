# Project 2 USI Pathfinder
CS311 Data Structures and Algorithms · Fall 2026
100 points · Course Projects · Due December 9, 2026 at 11:59 PM Central
Starter repository: [https://github.com/cwillpinto/cs311-project02-usi-pathfinder](https://github.com/cwillpinto/cs311-project02-usi-pathfinder)
Use **Use this template** under your own GitHub account. Python 3.11+; standard library only. USI Pathfinder Student.zip is a fallback.

## Mission
Build a routing engine for an illustrative USI campus. Buildings and junctions are vertices; undirected walkable connections are edges weighted in travel minutes. Find shortest routes using heap-based Dijkstra, then reroute when a connection closes. The supplied map is a teaching model, not measured campus navigation data. A* is a classroom comparison and is not required in the project.

## Part A Design and build the campus graph
1. Inspect campus_map_data.py. WAYPOINTS contains 10 unique IDs and coordinate pairs; EDGES contains 16 undirected connections with minute weights. Load these supplied Python structures; no external map service or CSV parser is required. Keep the data unchanged. Coordinates are map positions, not travel minutes.
2. Write DESIGN.md: diagram Graph, routing and simulation; describe adjacency storage, separate closure state, waypoint coordinates and schedule format. Explain how one route request reads the current closures. Use the Week 14 campus diagram, adjacency list and first-increment slides as the starting example.
3. Complete Graph in pathfinder.py. add_node creates an adjacency entry without losing existing edges. add_edge stores each nonnegative weighted connection in both directions. close_edge and reopen_edge update closed_edges without deleting base edges. neighbors returns only currently open connections. A closure applies to both directions.
4. Check both directions of SCI–UC at weight 3. BEC–SCI–UC costs 7. Apply the lecture graph method to the supplied project map; its node IDs and weights come from campus_map_data.py. Reserve about 2–3 hours for graph design, loading and these first checks.

## Work order
November 17: graph model, one verified route, closures and initial tests during the combined Tuesday lesson.
November 24: integrate schedules and inspect reroutes. No class November 26.
December 1/3: regression tests, complexity audit, reproducibility and peer review.
December 9: final submission. Earlier steps are progress targets, not additional graded deadlines. Plan about 10–14 hours including studio time; debugging time varies.

---PAGE---
## Part B Implement routing and rerouting
1. Implement dijkstra(graph, start, end) with heapq. Return (total_travel_time, ordered_path), or None if no route exists. This differs from the lecture example's (path, cost). For a known start equal to end return (0, [start]). Track best costs and parents; update both for a strict improvement and skip stale heap entries. All supplied weights are nonnegative.
2. Implement campus_route(map_graph, src, dest) as the primary routing entry point. Graph owns closure state; neither function accepts an extra closed_set or blockages argument. Each request creates fresh search records. Do not use a library shortest-path solver or a linear minimum-distance scan.
3. Verify SCI → UC returns cost 3. Close SCI–UC: SCI → LIB → UC costs 5. Reopen it: cost returns to 3. A route returned before closure remains a record of that earlier request. The base adjacency list must stay intact. The final project connections and studio slides at the end of the Week 14 deck show this transfer.
4. Run at least 10 supplied simulated schedules, each with three or more stops, through run_campus_sim.py. The simulator closes SCI–UC between schedules 5 and 6, recomputes earlier schedules, checks a forced change, and later reopens it. Keep the supplied simulator, data and tests unchanged.
5. Run python -m unittest -v test_pathfinder.py, then python run_campus_sim.py. The first run of the unchanged starter intentionally raises NotImplementedError. Complete pathfinder.py independently; the Examples folder contains the smaller lecture demonstration, not a finished project Graph implementation.
6. Exercise start=goal, an unreachable destination, a closure blocking the only route, reopening and repeated requests. Compare returned cost with the sum of open edges in the returned path. Equally short valid routes may differ. The supplied tests compare costs with an independent relaxation-based oracle on the campus map and small generated graphs.

## Part C Analyze and review
1. Submit Complexity_Audit.md or .pdf. Justify adjacency-list space O(V+E), neighbor filtering, closure/reopening, route reconstruction and Dijkstra's time/space costs. Define V and E. Explain the cost of routing a batch of schedule legs and why a heap helps on sparse maps compared with O(V²) minimum selection.
2. For heapq with duplicate entries, justify O((V+E) log V) for this simple graph model, or state the more general O((V+E) log(E+1)) bound and its assumptions. Include the cost of stale candidates; do not claim decrease-key or O(V) heap space if your implementation does not provide it.
3. Follow Peer Review.md. Cold-run a partner's repository, record one strength, one technical issue with a suggested fix, and one useful tip. Keep given and received notes, and write a 5–10 sentence reflection explaining what you changed or justified after review. This is part of Project 2, not another lab.

---PAGE---
## Rubric
Data structure implementation — 30 points: correct weighted adjacency list and min-heap use; closures separated from the base map; efficient operations and justified choices.
Algorithmic correctness — 25 points: shortest costs and valid reconstructed paths, dynamic rerouting, disconnected cases, only-route closure, start=goal and reopening.
Documentation and analysis — 25 points: README 5; system/design diagram 5; complexity analysis 15.
Code quality and modularity — 15 points: graph, search and simulation separation; clear names, types and explanations; no shortcut logic that violates the required structures.
Reproducible terminal verification — 5 points: clean documented run, unchanged supplied checks, and complete matching run evidence.
Required total: 100 points. Optional bonus up to +5 remains separate: useful route visualization, schedule stress testing beyond 10, or exceptionally specific peer review. Existing terminal-only rule remains: if the project requires an IDE to run or lacks CLI instructions in README.md, the grade is capped at 50%. Other course grading policies remain applicable.

## Submission in Blackboard
1. Your student-owned GitHub repository URL, final commit SHA, and v1.0-final tag. Keep meaningful development history. The instructor starter is an upstream source; push your work to your own repository. See README.md for the safe remote workflow. No GitHub Classroom is required.
2. Repository files: completed pathfinder.py; unchanged campus_map_data.py, run_campus_sim.py and test_pathfinder.py; DESIGN.md; README.md with exact terminal commands; Complexity_Audit.md or .pdf.
3. Peer review notes given and received, plus Peer_Review_Reflection.md (5–10 sentences). Use Peer_Review_Given.md and Peer_Review_Received.md or PDFs with the same names.
4. Paste your Final Token in Blackboard. Include a screenshot of the token output and the raw terminal log from the same run. Enter your own USI username when prompted. Do not include environments, Python caches, credentials or unrelated course work.

## What verification establishes
The simulator issues a token only after the supplied test suite and schedule/closure checks pass. The token covers those checks; it does not prove universal correctness or authorship. Explain your design and test any additional cases you identify. Tests check optimal cost and legal paths without requiring one particular tie-breaking route.
