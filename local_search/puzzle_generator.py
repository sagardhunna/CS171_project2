import time
from puzzle import Puzzle
import random
import math

# DO NOT modify any other source files, can add new member functions or variables to PuzzleGenerator class
# CAN use any local search algorithm so SIMLUATED ANNEALING or HILLCLIMBING

# first implement hillclimbing and get it to work, then try simulated annealing
# try including random restarts and storing the best solution i have found so far
# if current search for a good puzzle does not appear to be promising, might want to terminate early to save time

# CANNOT USE external libraries OTHER THAN math/random
# r and c will be between 5 and 10 inclusive

class PuzzleGenerator:
    def __init__(self, n_rows: int, n_columns: int, min_val: int, max_val: int):
        self.n_rows = n_rows
        self.n_columns = n_columns
        self.min_val = min_val
        self.max_val = max_val
        self.max_time = 59.9  # To make sure we don't exceed a minute

    # FUNCTION THAT WE ARE IMPLEMENTING TO GENERATE A GOOD PUZZLE
    def generate_puzzle(self) -> Puzzle:
        random_walk_time = 60.0 
        
        s = Puzzle(self.n_rows, self.n_columns, self.min_val, self.max_val)
        
        best_puzzle = s
        best_value = s.get_value()
                
        t_value = 100
        
        alpha =  0.9995
        
        
        start_time = time.time()
        total_iterations = 0
        taken_worse = 0
        iterations_less_than_300 = 0
        random_restarts = 0
                
        while time.time() - start_time < random_walk_time - 0.1:
            s_prime = s.get_random_successor()
            s_prime
                
            
            delta_e = s_prime.get_value() - s.get_value()
            
            rand = random.random()
            if delta_e / t_value <= 500:
                e = math.exp(delta_e / t_value)
            
            if delta_e > 0:
                s = s_prime
                if s.get_value() > best_value:
                    best_value = s.get_value()
                    best_puzzle = s
            elif rand < e:
                taken_worse += 1
                s = s_prime
                
                    
            t_value *= alpha
            
            if t_value <= 0.01: 
                t_value = 100
                
            if best_value <= 300: 
                iterations_less_than_300 += 1
            
            if iterations_less_than_300 >= 4000 and self.n_columns > 5:
                s = Puzzle(self.n_rows, self.n_columns, self.min_val, self.max_val)
                iterations_less_than_300 = 0
                random_restarts += 1
                
            if s.get_value() > best_value:
                best_value = s.get_value()
                best_puzzle = s
            
            total_iterations += 1
                
        print(f'Total iterations: {total_iterations} -- Taken worse: {taken_worse} -- Taken better: {total_iterations - taken_worse} -- random restarts : {random_restarts} ')
        return best_puzzle

    # PROVIDED FUNCTION ALREADY GENERATES BETTER THAN AVERAGE PUZZLES, look at source code
    # to understand how to use the Puzzle class
    def random_walk(self, time_limit: float) -> Puzzle:
        # A very simple function that starts at a random configuration and keeps randomly modifying it
        # until it hits the time limit. Returns the best solution found so far.
        
        p = Puzzle(self.n_rows, self.n_columns, self.min_val, self.max_val)  # Generate a random puzzle
        
        # Keep track of the best puzzle found so far (and its value)
        best_puzzle = p
        best_value = p.get_value()
        
        # Keep track of the time so we don't exceed it
        start_time = time.time()
        
        # Loop until we hit the time limit
        while time.time() - start_time < time_limit - 0.1:  # To make sure we don't exceed the time limit
            # Generate a successor of p by randomly changing the value of a random cell
            # (since we are doing a random walk, we just replace p with its successor)
            p = p.get_random_successor()
            value = p.get_value() 
            
            # Update the current best solution
            if value > best_value:  
                best_value = value  
                best_puzzle = p
        
        return best_puzzle 