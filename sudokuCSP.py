import os
import sys
import copy
class SudokuCSP:
    def __init__(self, filename):
        self.board = self.read_board(filename)
        self.variables = [(r, c) for r in range(9) for c in range(9)]
        self.domains = {}
        self.neighbors = {var: set() for var in self.variables}
        self.backtrack_calls = 0
        self.backtrack_failures = 0
        for r, c in self.variables:
            val = self.board[r][c]
            if val == 0:
                self.domains[(r, c)] = set(range(1, 10))
            else:
                self.domains[(r, c)] = {val}
        self._setup_neighbors()
    def read_board(self, filename):
        board = []
        try:
            with open(filename, 'r') as f:
                for line in f:
                    stripped = line.strip()
                    if stripped:
                        board.append([int(char) for char in stripped])
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
            sys.exit(1)
        return board
    def _setup_neighbors(self):
        for r, c in self.variables:
            for i in range(9):
                if i != c: self.neighbors[(r, c)].add((r, i))
                if i != r: self.neighbors[(r, c)].add((i, c))
            block_r, block_c = 3 * (r // 3), 3 * (c // 3)
            for i in range(3):
                for j in range(3):
                    if (block_r + i, block_c + j) != (r, c):
                        self.neighbors[(r, c)].add((block_r + i, block_c + j))
    def revise(self, xi, xj):
        revised = False
        for x in list(self.domains[xi]):
            if len(self.domains[xj]) == 1 and x in self.domains[xj]:
                self.domains[xi].remove(x)
                revised = True
        return revised
    def ac3(self):
        queue = [(xi, xj) for xi in self.variables for xj in self.neighbors[xi]]
        while queue:
            xi, xj = queue.pop(0)
            if self.revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False
                for xk in self.neighbors[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True
    def select_unassigned_variable(self, domains):
        unassigned = [v for v in self.variables if len(domains[v]) > 1]
        if not unassigned:
            return None
        return min(unassigned, key=lambda v: len(domains[v]))
    def forward_check(self, var, value, domains):
        new_domains = copy.deepcopy(domains)
        for neighbor in self.neighbors[var]:
            if value in new_domains[neighbor]:
                new_domains[neighbor].remove(value)
                if len(new_domains[neighbor]) == 0:
                    return None 
        return new_domains
    def backtrack(self, domains):
        self.backtrack_calls += 1
        var = self.select_unassigned_variable(domains)
        if var is None:
            return domains
        for value in domains[var]:
            new_domains = self.forward_check(var, value, domains)
            if new_domains is not None:
                new_domains[var] = {value} 
                result = self.backtrack(new_domains)
                if result is not False:
                    return result
        self.backtrack_failures += 1
        return False
    def solve(self):
        if not self.ac3():
            return False
        solution = self.backtrack(self.domains)
        if solution:
            solved_board = [[0]*9 for _ in range(9)]
            for (r, c), val_set in solution.items():
                solved_board[r][c] = list(val_set)[0]
            return solved_board
        return False
    def print_board(self, board):
        for r in range(9):
            if r % 3 == 0 and r != 0:
                print("- - - - - - - - - - -")
            row_str = ""
            for c in range(9):
                if c % 3 == 0 and c != 0:
                    row_str += "| "
                row_str += str(board[r][c]) + " "
            print(row_str)
if __name__ == "__main__":
    files = ["easy.txt", "medium.txt", "hard.txt", "veryhard.txt"]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for file in files:
        print(f"\n====================\nSolving {file}...\n====================")
        file_path = os.path.join(script_dir, file)
        solver = SudokuCSP(file_path)
        solution = solver.solve()
        if solution:
            solver.print_board(solution)
        else:
            print("No solution found.")
        print(f"Calls to BACKTRACK: {solver.backtrack_calls}")
        print(f"BACKTRACK failures: {solver.backtrack_failures}")