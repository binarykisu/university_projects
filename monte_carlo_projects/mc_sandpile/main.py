import numpy as np 
from random import random, choice
import matplotlib.pyplot as plt

def initialize_grid(num_sites:int):
    """
    Step 1 - Initialize the sandpile grid with zeros.
    """
    return np.zeros(num_sites+2)
    
def add_grain(grid:list):
    """
    Rule: Step 1 - Add a grain to the left-most site.
    """
    grid[len(grid)//2] += 1
    print(f"Added left-most grain -> {grid}")
    
def drop_grains(grid, num_sites:int):
    """
    Drop grains randomly everywhere in the interval [1, num_sites].
    """
    site = choice(range(1, num_sites))  # Choose a random site to drop grain
    grid[site] += 1
    print(f"Added grain to site {site} -> {grid}")

def topple(grid, num_sites:int):
    """
    Rule: Step 2 - 4 - Mark sites for toppling if h(i) - h(i + 1) > 2 and topple them to the right.
    """ 
    toppled = False
    for i in range(len(grid)): # run through all 12 sites
        # print(f"site: {i}")
        if i == 0 or i == len(grid) - 1:
            # print(f"At site {i}, setting grains to 0.")
            grid[i] = 0
        elif int(grid[i]) - int(grid[i + 1]) > 2: # mark site for toppling
            # print(f"{int(grid[i])} - {int(grid[i + 1])} > 1")
            toppled = True
            print(f"Toppled!")            
            direction = choice([-1, 1]) # randomly choose left or right direction
            # print(f"Direction to topple: {direction}")
            grid[i] -= 2
            grid[i + direction] += 1
            if abs(int(grid[i]) - int(grid[i + 1])) == 1: # if only 3 larger on one side
                grid[i + 2*direction] += 1
    plot_sandpile(grid)  # Call plot_sandpile after toppling
    return toppled

def plot_sandpile(grid):
    """
    Visualize the sandpile with grains represented by '¤' and empty sites represented by spaces.
    """
    max_height = int(max(grid))
    print(f"\nMax height of sandpile: {max_height}\n")
    
    if max_height <= 0:  # If sandpile is empty, print only the horizontal axis
        print('+' + '-'*len(grid)*3 + '+')
        return
    
    for height in reversed(range(max_height + 1)):
        #row = f'    |'
        row = f'|'
        for site in grid[1:-1]:  # Exclude boundary sites
            if int(site) > height:
                row += ' ¤ '
            else:
                row += '   '
        print(row + ' |')
    print('+' + '-' * len(row) + '+')

def run_sandpile(num_sites:int, iterations:int):
    grid = initialize_grid(num_sites)
    for iter in range(iterations):
        print(f"\nIteration: {iter+1}")
        # add_grain(grid) # If you want grains dropped on the left-most site only
        drop_grains(grid, num_sites)  # Drop grains randomly across the sandpile
        topple(grid, num_sites)


if __name__ == "__main__":
    iterations = 20  
    num_sites = 10 # number of sites
    run_sandpile(num_sites, iterations)
