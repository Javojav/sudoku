import random
import display as disp
import sys
import numpy as np

defaultGrid = [
    [0, 0 ,0, 0, 0 ,0, 2, 0 ,0],
    [0, 8 ,0, 0, 0 ,7, 0, 9 ,0],
    [6, 0 ,2, 0, 0 ,0, 5, 0 ,0],
    [0, 7 ,0, 0, 6 ,0, 0, 0 ,0],
    [0, 0 ,0, 9, 0 ,1, 0, 0 ,0],
    [0, 0 ,0, 0, 2 ,0, 0, 0 ,0],
    [0, 0 ,5, 0, 0 ,0, 6, 0 ,3],
    [0, 9 ,0, 4, 0 ,0, 0, 7 ,0],
    [0, 0 ,6, 0, 0 ,0, 0, 0 ,0],
]


def possible(grid, x, y, n):
    # horizontal
    for i in range(0, 9):
        if i == x:
            continue

        if grid[y][i] == n:
            return False

    # vertical
    for i in range(0, 9):
        if i == y:
            continue

        if grid[i][x] == n:
            return False
    
    # square
    firstX, firstY = x//3 * 3, y//3 * 3 # find first position of the square

    for i in range(0, 3):
        for j in range(0, 3):
            currX, currY = i + firstX, j + firstY

            if currX == x and currY == y:
                continue
            
            if grid[currY][currX] == n:
                return False
    
    return True


def solve(grid, display=False, shufflePossible=False, displayHideNumbers=False):
    for x in range(0,9):
        for y in range(0,9):
            # find empty square
            if grid[y][x] == 0:
                possibleSolutions = [n for n in range(1, 10) if possible(grid, x, y, n)] # find possible solutions
                if shufflePossible:
                    random.shuffle(possibleSolutions) # shuffle possible solutions (mainly for randomGrid)

                for attempt in possibleSolutions:
                    grid[y][x] = attempt # try solution

                    if solve(grid, display=display, shufflePossible=shufflePossible, displayHideNumbers=displayHideNumbers): 
                        return grid # solution found

                    if display:
                        disp.displayGrid(grid, x, y, hideNumbers=displayHideNumbers)
                    
                    grid[y][x] = 0 # reset square
                
                return False # attempts failed, backtrack

    return grid


# generate a random grid with a given number of clues
# useSolveAfter: after a given number of randomly placed numbers the grid will be solved
#                to ensure that the grid is solvable if it isnt the function will be called again
# using a low number in useSolveAfter will result in a less randomized grid
# using a high number in useSolveAfter will result in more failed attempts thus a slower runtime
def randomGrid(clues, useSolveAfter=10, display=False):
    grid = [[0 for _ in range(0, 9)] for _ in range(0, 9)] # create empty grid

    free = [(x, y) for x in range(0, 9) for y in range(0, 9)] # list of free positions
    random.shuffle(free) # shuffle list

    placed = 0 

    while placed < useSolveAfter:
        x, y = free.pop() # get random free position

        n = random.randint(1, 9) # random number

        if display:
            disp.displayGrid(grid, x, y, hideNumbers=True)

        while not possible(grid, x, y, n): # find a possible number
            n = random.randint(1, 9)

        grid[y][x] = n # insert number

        placed += 1
    
    grid = solve(grid, display=display, shufflePossible=True, displayHideNumbers=True) # solve grid

    if grid == False:
        grid = randomGrid(clues, useSolveAfter)


    removeNums = [(x, y) for x in range(0, 9) for y in range(0, 9)] # list of positions to remove numbers from
    random.shuffle(removeNums) # shuffle list

    removeNums = removeNums[: 81 - clues] # get first n positions 

    for x, y in removeNums:
        grid[y][x] = 0

    return grid



if __name__ == "__main__":
    if "-r" in sys.argv:
        sol = randomGrid(50, display=True)
        disp.displayGrid(sol)
    else:
        solution = solve(defaultGrid, display=True)
        disp.displayGrid(solution)