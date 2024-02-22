import numpy as np 
from random import random, choice
import matplotlib.pyplot as plt

def initialize_grid(num_sites:int):
    """
    Step 0: Initialize the sandpile grid with zeros.
    """
    return np.zeros(num_sites+2) # Grid of length, L
    
def add_grain(grid:list) -> None:
    """
    Step 1: Add a grain to the middle site of the grid.
    """
    grid[len(grid)//2] += 1 # Choose the middle of the grid
    print(f"Added grain to site {site}")
    
def drop_grains(grid, num_sites:int) -> None:
    """
    Modification to Step 1: Drop grains randomly across the grid interval.
    """
    site = choice(range(1, num_sites))  # Choose a random site 
    grid[site] += 1
    print(f"Added grain to site {site}")

def topple(grid, num_sites:int) -> None:
    """
    Step 2 - 4: Mark sites for toppling if h(i) - h(i + 1) > 2 and topple them to the left or right.
    """ 
    toppled = False
    for i in range(len(grid)): # Run through all grid sites
        # print(f"site: {i}") # For testing
        if i == 0 or i == len(grid) - 1: # Grains past the set number of sites are lost forever (= 0)
            # print(f"At site {i}, setting grains to 0.") # For testing
            grid[i] = 0
        elif int(grid[i]) - int(grid[i + 1]) > 2: # Mark site for toppling
            toppled = True
            print(f"Toppled!")            
            direction = choice([-1, 1]) # Randomly choose left or right direction
            # print(f"Direction to topple: {direction}") # For testing
            grid[i] -= 2
            grid[i + direction] += 1
            if abs(int(grid[i]) - int(grid[i + 1])) == 1: # If only 3 larger on one side
                grid[i + 2*direction] += 1
    plot_sandpile(grid)  # Call plot_sandpile after toppling

def plot_sandpile(grid) -> None:
    """
    Visualizes the sandpile with grains represented by '¤' in the console/terminal.
    """
    max_height = int(max(grid)) # Height of plot
    print(f"\n| = Lost forever\nMax height of sandpile: {max_height}\n") # Plot information
    
    if max_height <= 0:  # If sandpile is empty, print only the x-axis
        print('+' + '-' * len(grid) * 3 + '+') # x-axis
        return
    
    for height in reversed(range(max_height + 1)): 
        row = f'|'
        for site in grid[1 : -1]:  # Exclude boundary sites
            if int(site) > height:
                row += ' ¤ ' # Print if grain is present
            else:
                row += '   ' # Grain not present here
        print(row + ' |') # Boundaries/lost forever
    print('+' + '-' * len(row) + '+') # x-axis

def run_sandpile(num_sites:int, iterations:int) -> None:
    """
    Main function to run the sandpile program.
    Inputs: num_sites = size of grid; iterations = how many seeds are added to the sandpile
    """
    grid = initialize_grid(num_sites) # This is the h(i) function
    for iter in range(iterations):
        print(f"\nIteration: {iter + 1}")
        # add_grain(grid) # If you want grains dropped in the middle of the grid
        drop_grains(grid, num_sites)  # Drop grains randomly across the sandpile
        topple(grid, num_sites) # Checks/handles sites to see if they need to be toppled

if __name__ == "__main__":
    iterations = 50  # Desired number of iterations
    num_sites = 15 # Number of sites
    run_sandpile(num_sites, iterations) # Runs the sandpile simulation
