import sys
import time
from puzzle_generator import PuzzleGenerator

def main():
    # Process the arguments
    if len(sys.argv) != 5:
        print("Please specify the number of rows and columns and the minimum and maximum values for each cell (requires 4 parameters)")
        sys.exit(1)
    
    n_rows = int(sys.argv[1])
    n_columns = int(sys.argv[2])
    min_val = int(sys.argv[3])
    max_val = int(sys.argv[4])

    # Start the timer
    start_time = time.time()
    
    # Generate the puzzle
    print(f"Generating a {n_rows}x{n_columns} puzzle with values in range [{min_val}-{max_val}]")
    
    generator = PuzzleGenerator(n_rows, n_columns, min_val, max_val)
    puzzle = generator.generate_puzzle()
    puzzle.print_puzzle(True)
    
    # Print the elapsed time
    elapsed_time = time.time() - start_time
    print(f"Total time: {elapsed_time:.6f} seconds")

if __name__ == "__main__":
    main() 