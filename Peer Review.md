# USI Pathfinder Peer Review
CS311 · Project 2 · Due with the final project December 9, 2026 at 11:59 PM Central

## Cold start
Work with the classmate assigned in class or Blackboard. Clone their student-owned repository into a clean folder. Follow only their README.md. Run python -m unittest -v test_pathfinder.py and python run_campus_sim.py. Record the repository URL, commit SHA, commands and actual results. Never place another person's username in your own submission evidence.

## Review checklist
1. Inspect how the supplied 10-waypoint map becomes a weighted adjacency list. Each undirected edge should be stored both ways; coordinates do not define travel times.
2. Check heapq-based Dijkstra, relaxation, stale entries and start-to-destination reconstruction. Inspect at least one returned path and cost independently.
3. Check SCI–UC before closure (3), after closure via LIB (5), and after reopening (3). Inspect preserved base edges and the behavior of disconnected/only-route cases.
4. Run the full 10-schedule simulation; trace at least one multi-stop schedule. Distinguish observed tests from claims you did not verify.
5. Check the complexity audit's model, sparse-graph comparison, duplicate heap entries and batch routing costs.

## Written feedback and response
Give three specific comments: one strength with evidence, one technical issue with a suggested fix, and one useful tip. If no defect is observed, identify a concrete coverage or explanation improvement rather than inventing a failure. Save Peer_Review_Given.md or .pdf; retain the received review as Peer_Review_Received.md or .pdf. Write Peer_Review_Reflection.md, 5–10 sentences explaining what you changed or justified after the review.

## Final verification
Re-run both commands after your fixes. Commit your files, tag the final commit v1.0-final, and push to your own repository. Submit the URL, SHA, Final Token, matching screenshot and raw log with the other project files through Blackboard. The token verifies supplied checks, not every possible input. This review is part of Project 2; it adds no separate lab or intermediate graded deadline.
