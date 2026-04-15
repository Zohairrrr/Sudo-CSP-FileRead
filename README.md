Overview
This project implements a Sudoku solver using Constraint Satisfaction Problem (CSP)
techniques in Python. It efficiently solves Sudoku puzzles of varying difficulties by
combining intelligent search algorithms and constraint propagation.

Algorithmic Methodology (Step-by-Step)
Step 1: Problem Formulation
Variables: The 81 cells on the 9x9 grid.
Domains: The possible integer values for each cell (1-9 for empty cells, a specific single
value for pre-filled cells).
Constraints: The standard Sudoku rules enforced via binary constraints—no duplicate
numbers in any shared row, column, or 3x3 block.
Step 2: Pre-processing with AC-3
Before initiating the main search tree, the solver runs the Arc Consistency 3 algorithm. This
systematically evaluates pairs of neighboring cells and reduces their domains by
eliminating values that lack a valid match.
Step 3: Variable Selection via MRV
The algorithm uses the Minimum Remaining Values (MRV) heuristic to carefully select the
next empty cell to process, actively minimizing the search tree size.
Step 4: Backtracking Search with Forward Checking
The core engine relies on a depth-first backtracking search. Forward Checking looks ahead
and removes assigned values from neighboring domains, instantly recognizing
mathematical invalidities and backtracking.

Setup and Requirements
• Python 3.6 or higher is required.
• No external dependencies or libraries are needed.

Usage
1. Ensure your Sudoku puzzle files (e.g., easy.txt, hard.txt) are in the same directory as the
script.
2. Run the script from your terminal:
python sudokuCSP.py
