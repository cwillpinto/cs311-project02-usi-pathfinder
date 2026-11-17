# Project 2 USI Pathfinder

CS311 · 100 points · Due December 9, 2026 at 11:59 PM Central

Build a campus routing program that finds shortest routes and handles closed connections. Read **Project 2 USI Pathfinder.pdf** for the assignment and rubric, and **Peer Review.md** for the review instructions. The map uses familiar USI names with made-up connections and walking times.

## Get started

Open https://github.com/cwillpinto/cs311-project02-usi-pathfinder and choose **Use this template**. Create the new repository under your own account, then clone it to your computer. If you use the ZIP instead, extract it and add the files to your own repository.

You need Python 3.11 or later. There are no packages to install. From the project folder, run:

```sh
python -m unittest -v test_pathfinder.py
python run_campus_sim.py
```

The starter raises `NotImplementedError` until you finish the missing methods and functions in `pathfinder.py`. Keep `campus_map_data.py`, `test_pathfinder.py`, and `run_campus_sim.py` unchanged.

## Build and check your routes

Complete `Graph`, `dijkstra`, and `campus_route`. Use `heapq` for Dijkstra's priority queue. A* is covered in class but is not required for this project.

Start with SCI → UC. The cost should be 3. Close that connection and check the route through LIB, which costs 5. Reopen it and check that the cost returns to 3. BEC → UC should change from 7 to 9 when SCI–UC is closed.

Store closures in `Graph.closed_edges`; keep the original adjacency list intact. Each route request should use the current closures and leave previously returned results alone. Return `(travel_time, path)`, or `None` when no route exists.

## Files

- `pathfinder.py`: the graph and routing code you complete.
- `campus_map_data.py`: 10 waypoints and 16 undirected connections. Coordinates describe positions; edge weights give travel minutes.
- `test_pathfinder.py`: checks for shortest routes, legal paths, closures, and repeated requests.
- `run_campus_sim.py`: runs the tests and 10 schedules, then prints a Final Token if its checks pass.
- `Project 2 USI Pathfinder.md/.docx/.pdf`: the assignment, rubric, and submission checklist.
- `Peer Review.md`: instructions for reviewing a classmate's project.
- `Examples/pathfinding_demo.py` and `Examples/Pathfinding Code Guide.md`: the smaller example from class and its line-by-line explanation.

Run the class example with `python Examples/pathfinding_demo.py`. It compares the original route, the quad shortcut, and a closed connection. Its functions return `(path, cost)`; the project functions return `(travel_time, path)`.

## If you clone the instructor repository directly

Create an empty repository under your own account first. Then run these commands, replacing `<your-repository-url>` with its URL:

```sh
git clone https://github.com/cwillpinto/cs311-project02-usi-pathfinder
cd cs311-project02-usi-pathfinder
git remote rename origin upstream
git remote add origin <your-repository-url>
git remote -v
git branch --show-current
git push -u origin main
```

Before pushing, check that `origin` is your repository and `upstream` is the instructor's. If your branch has a different name, use that name instead of `main`.

## Submit in Blackboard

Submit your repository URL, final commit SHA, and `v1.0-final` tag. Include the completed code, supplied data/tests/simulator, `DESIGN.md`, a README with run instructions, and `Complexity_Audit.md` or `.pdf`.

Also include `Peer_Review_Given.md`/`.pdf`, `Peer_Review_Received.md`/`.pdf`, and `Peer_Review_Reflection.md` (5–10 sentences). Paste the Final Token in Blackboard and attach a screenshot and raw terminal log from the same run. Enter your own USI username when prompted.

Keep your development history. Leave out Python caches, virtual environments, and credentials. Passing the supplied checks is required, but you should also test the additional cases described in the handout. The handout contains the full rubric and terminal-only grading rule.
