# Project 2 USI Pathfinder

CS311 · 100 points · Course Projects · due December 9, 2026 at 11:59 PM Central.
Read **Project 2 USI Pathfinder.md** and **Peer Review.md**, supplied here. The map uses USI building names with illustrative connections and travel minutes. It is not actual campus navigation data. Implement Dijkstra; A* is comparison material only.

## Starter repository

https://github.com/cwillpinto/cs311-project02-usi-pathfinder

Choose **Use this template** to create a repository under your own account, then clone your new repository. The ZIP is a contingency download.

## Start
Use Python 3.11+; no third-party dependencies. From this directory:

```sh
python -m unittest -v test_pathfinder.py
python run_campus_sim.py
```

The unchanged starter intentionally fails with NotImplementedError. Complete `Graph`, `dijkstra`, and `campus_route` in `pathfinder.py`. Keep `campus_map_data.py`, `test_pathfinder.py`, and `run_campus_sim.py` unchanged. The simulator runs the supplied tests before issuing its Final Token. A token covers those checks, not universal correctness or authorship.

## First check
SCI to UC costs 3. Closing SCI–UC forces SCI–LIB–UC at cost 5; reopening restores 3. BEC to UC changes from 7 to 9 while that edge is closed. Preserve base adjacency and old returned route records. Project return value is `(travel_time, path)`, or `None` if unreachable. No extra closure argument: the Graph owns `closed_edges`.

## Files
- `campus_map_data.py`: 10 waypoints, 16 undirected weighted edges; coordinates are map units, weights are minutes.
- `pathfinder.py`: intentionally incomplete graph and routing implementation.
- `test_pathfinder.py`: route validity, optimal cost and closure/regression checks.
- `run_campus_sim.py`: supplied 10-schedule simulation and Final Token.
- `Project 2 USI Pathfinder.md/.docx/.pdf`: full assignment.
- `Peer Review.md`: cold-run, feedback and reflection process.
- `Examples/pathfinding_demo.py`: near-BEC lecture example; run `python Examples/pathfinding_demo.py`. It returns `(path, cost)`, unlike the project interface. It is not a finished project implementation.

## Work in your own repository
Use the instructor template above: choose **Use this template** under your own account, then clone your new repository. For the attached ZIP fallback, extract it, create your own empty GitHub repository, initialize Git locally, commit, and add your student-owned URL as origin. Verify `git remote -v` before pushing.

If directly cloning an instructor starter instead of using a template, create your own empty repository first, then replace the student-owned URL placeholder below with your own URL:

```sh
git clone https://github.com/cwillpinto/cs311-project02-usi-pathfinder
cd cs311-project02-usi-pathfinder
git remote rename origin upstream
git remote add origin <student-owned-repository-url>
git remote -v
git branch --show-current
git push -u origin main
```

Use your actual branch name if it is not main. The instructor repository is upstream; push completed work only to your own origin. The verified instructor template above is the upstream source; completed work belongs in your own repository.

## Submit in Blackboard
Submit your student-owned repository URL and final commit SHA, with final commit tagged `v1.0-final`. Include `DESIGN.md`, completed `pathfinder.py`, supplied data/tests/simulator, a README with terminal instructions, `Complexity_Audit.md` or `.pdf`, `Peer_Review_Given.md`/`.pdf`, `Peer_Review_Received.md`/`.pdf`, and `Peer_Review_Reflection.md` (5–10 sentences). Paste the Final Token and include a screenshot plus the raw log from the same run. Preserve meaningful commit history; omit caches, environments and credentials. See the handout for the approved rubric and terminal-only grading rule.

## Code walkthrough

The lecture example uses BEC, Liberal Arts (LA), Arts Center (AC), Starbucks at Rice Library (SB), and Chick-fil-A at UC West (CF). Its links and minute weights are illustrative; the full project keeps the original supplied dataset and node IDs. Starbucks and Chick-fil-A are not sponsors of these slides or example.

Read `Examples/Pathfinding Code Guide.md` for every line, symbol and return value. `Examples/pathfinding_demo.py` contains the same complete functions with explanatory comments. Run `python Examples/pathfinding_demo.py`: both algorithms return the BEC–LA–CF route at 7 illustrative minutes. These lecture functions return `(path, cost)`; the project returns `(travel_time, path)` or `None`.
