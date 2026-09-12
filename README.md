Ponder Color Flood Solver

A solver for the daily Color Flood puzzle on Ponder Club. It scrapes the current board from the live page, reconstructs it as a grid, and computes a solution using a greedy heuristic. An exact solver and heuristic comparison planned next.

How it works:
Scrapes ponderclub.co: Playwright (Firefox) loads the puzzle page and screenshots the color grid.
Parses the image: OpenCV samples each cell and matches it against the known palette to build a 10x10 grid of colors.
Solves the daily game: starting from the top-left cell, a greedy heuristic repeatedly grows the captured region by choosing the most popular color among the currently adjacent cells until the whole board is one color.

Current algorithms available:
chain_theory():  greedy, chooses the most frequent adjacent color at each step. Fast, but not guaranteed optimal.

Upcoming algorithms:
a_star(): IDA* or Iterative Deepening A* over a region graph, using shortest-path-to-farthest-region to hopefully find true optimal move count, then benchmarking the greedy heuristic and future solvers against it.

Requirements:
pip install -r requirements.txt
playwright install firefox

Usage:
python solver.py in Visual Studio Code

Status:
Personal project, actively evolving. Next steps: region-graph representation, exact solver, and a comparison of moves-used and runtime across algorithms.
