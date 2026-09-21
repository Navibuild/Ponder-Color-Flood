Ponder Color Flood Solver

A solver for the daily Color Flood puzzle on Ponder Club. It scrapes the current board from the live page, reconstructs it as a grid, and computes a solution using a greedy heuristic. An exact solver and heuristic comparison planned next.

How it works:
Scrapes ponderclub.co: Playwright (Firefox) loads the puzzle page and screenshots the color grid.
Parses the image: OpenCV samples each cell and matches it against the known palette to build a 10x10 grid of colors.
Solves the daily game: starting from the top-left cell, a greedy heuristic repeatedly grows the captured region by choosing the most popular color among the currently adjacent cells until the whole board is one color.

Current algorithms available:
solver("Greedy"): Greedy, chooses the most frequent adjacent color at each step. Fast, but not guaranteed optimal.
solver("IDA*"): IDA* or Iterative Deepening A* over a region graph, using shortest-path-to-farthest-region to find the true optimal move count.

Upcoming algorithms:
Beam search, plain A*, and MCTS

Requirements:
pip install -r requirements.txt
playwright install firefox

Usage:
python solver.py in Visual Studio Code

Status:
Personal project, actively evolving. Next steps: Comparing different algorithms against each other for time vs accuracy.
