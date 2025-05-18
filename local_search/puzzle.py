import random
from typing import List, Tuple

class PCell:
    def __init__(self, val: int = 1):
        self.val = val
        self.succ: List[int] = []
        self.pred: List[int] = []
        self.g_val = 0
        self.unique_path = True
        self.reachable = False
        self.reaching = False

class Puzzle:
    def __init__(self, n_rows: int, n_columns: int, min_val: int, max_val: int):
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.min_val = min_val
        self.max_val = max_val
        self.p_size = n_rows * n_columns
        self.cells = [PCell() for _ in range(self.p_size)]
        self.evaluated = False
        self.randomize()

    def get_value(self) -> int:
        if not self.evaluated:
            self.evaluate()
        return self.value

    def has_solution(self) -> bool:
        if not self.evaluated:
            self.evaluate()
        return self.has_solution_flag

    def get_random_successor(self) -> 'Puzzle':
        p = Puzzle(self.n_rows, self.n_columns, self.min_val, self.max_val)
        p.cells = [PCell(cell.val) for cell in self.cells]
        
        if self.min_val == self.max_val:  # Can't change anything
            return p
            
        # Pick a random cell
        i = random.randint(0, self.p_size - 2)  # Don't modify the goal
        
        # Randomly change its value
        new_val = self.cells[i].val
        while new_val == self.cells[i].val:
            new_val = random.randint(self.min_val, self.max_val)
        
        p.set_cell_value(i, new_val)
        return p

    def get_all_successors(self) -> List['Puzzle']:
        successors = []
        for i in range(self.p_size - 1):  # Do not modify the goal!
            for v in range(self.min_val, self.max_val + 1):
                if self.cells[i].val != v:
                    p = Puzzle(self.n_rows, self.n_columns, self.min_val, self.max_val)
                    p.cells = [PCell(cell.val) for cell in self.cells]
                    p.set_cell_value(i, v)
                    successors.append(p)
        return successors

    def randomize(self):
        # Randomly initialize the puzzle
        for i in range(self.p_size):
            self.cells[i].val = random.randint(self.min_val, self.max_val)
        
        # Set the goal to be 0
        self.cells[self.p_size - 1].val = 0
        self.evaluated = False

    def set_cell_value(self, cell: int, val: int):
        self.cells[cell].val = val
        self.evaluated = False

    def print_puzzle(self, print_statistics: bool = True):
        if not self.evaluated:
            self.evaluate()

        print("\nPuzzle:\n")
        i = 0
        for r in range(self.n_rows):
            row_vals = []
            for c in range(self.n_columns):
                row_vals.append(f"{self.cells[i].val:>3}") 
                i += 1
            print(" ".join(row_vals))
        print()

        if print_statistics:
            print(f"Solution: {'Yes' if self.has_solution_flag else 'No'}")
            print(f"Unique: {'Yes' if self.has_unique_solution else 'No'}")
            print(f"Solution length: {self.solution_length}")
            print(f"# of black holes: {self.n_black_holes}")
            print(f"# of white holes: {self.n_white_holes}")
            print(f"# of forced forward moves: {self.n_forced_forward_moves}")
            print(f"# of forced backward moves: {self.n_forced_backward_moves}")
            print(f"Puzzle value: {self.value}\n")

    def evaluate(self):
        self.generate_edges()
        
        self.n_black_holes = 0
        self.n_white_holes = 0
        self.n_forced_forward_moves = 0
        self.n_forced_backward_moves = 0
        self.n_reachable_cells = 0
        self.n_reaching_cells = 0

        for i in range(self.p_size):
            self.cells[i].reachable = False
            self.cells[i].reaching = False
            self.cells[i].unique_path = True
            self.cells[i].g_val = self.p_size

        self.forward_search()
        
        self.has_solution_flag = self.cells[self.p_size - 1].reachable
        self.solution_length = self.cells[self.p_size - 1].g_val
        self.has_unique_solution = (self.has_solution_flag and self.cells[self.p_size - 1].unique_path)
        
        self.backward_search()
        
        for i in range(1, self.p_size - 1):
            if self.cells[i].reachable:
                self.n_reachable_cells += 1
                if not self.cells[i].reaching:
                    self.n_black_holes += 1
                    
                if len(self.cells[i].succ) == 1:
                    self.n_forced_forward_moves += 1
            
            if self.cells[i].reaching:
                self.n_reaching_cells += 1
                if not self.cells[i].reachable:
                    self.n_white_holes += 1
                    
                if len(self.cells[i].pred) == 1:
                    self.n_forced_backward_moves += 1

        if len(self.cells[0].succ) == 1:
            self.n_forced_forward_moves += 1
        if len(self.cells[self.p_size - 1].pred) == 1:
            self.n_forced_backward_moves += 1
            
        self.compute_value()
        
        self.evaluated = True

    def compute_value(self):
        self.value = 0
        if not self.has_solution_flag:
            self.value -= self.p_size * 100
            
        if self.has_unique_solution:
            self.value += self.p_size
            
        self.value += self.solution_length * 5
        self.value -= 2 * (self.n_black_holes + self.n_white_holes + 
                          self.n_forced_forward_moves + self.n_forced_backward_moves)

    def generate_edges(self):
        for i in range(self.p_size):
            self.cells[i].succ.clear()
            self.cells[i].pred.clear()
        
        for i in range(self.p_size - 1):  # Exclude the goal
            r = i // self.n_columns
            c = i % self.n_columns
            x = self.cells[i].val
            
            if r + x < self.n_rows:  # Downward move
                self.add_edge(r, c, r + x, c)
                
            if r >= x:  # Upward move
                self.add_edge(r, c, r - x, c)

            if c + x < self.n_columns:  # Right move
                self.add_edge(r, c, r, c + x)
                
            if c >= x:  # Left move
                self.add_edge(r, c, r, c - x)

    def add_edge(self, r1: int, c1: int, r2: int, c2: int):
        i1 = r1 * self.n_columns + c1
        i2 = r2 * self.n_columns + c2
        self.cells[i1].succ.append(i2)
        self.cells[i2].pred.append(i1)

    def forward_search(self):
        queue = [0]  # Start from the first cell
        self.cells[0].reachable = True
        self.cells[0].g_val = 0
        
        while queue:
            current = queue.pop(0)
            for next_cell in self.cells[current].succ:
                if not self.cells[next_cell].reachable:
                    self.cells[next_cell].reachable = True
                    self.cells[next_cell].g_val = self.cells[current].g_val + 1
                    queue.append(next_cell)
                elif self.cells[next_cell].g_val == self.cells[current].g_val + 1:
                    self.cells[next_cell].unique_path = False

    def backward_search(self):
        queue = [self.p_size - 1]  # Start from the goal
        self.cells[self.p_size - 1].reaching = True
        
        while queue:
            current = queue.pop(0)
            for prev_cell in self.cells[current].pred:
                if not self.cells[prev_cell].reaching:
                    self.cells[prev_cell].reaching = True
                    queue.append(prev_cell) 