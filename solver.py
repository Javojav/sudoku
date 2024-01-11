import copy
import random
import display as disp
import sys
import numpy as np
import os
import time

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


def solve(grid, display=False, shufflePossible=False, displayHideNumbers=False, default=None, message=""):
    for x in range(0,9):
        for y in range(0,9):
            # find empty square
            if grid[y][x] == 0:
                possibleSolutions = [n for n in range(1, 10) if possible(grid, x, y, n)] # find possible solutions
                if shufflePossible:
                    random.shuffle(possibleSolutions) # shuffle possible solutions (mainly for randomGrid)

                for attempt in possibleSolutions:
                    grid[y][x] = attempt # try solution

                    if solve(grid, display=display, shufflePossible=shufflePossible, displayHideNumbers=displayHideNumbers, default=default, message=message): 
                        return grid # solution found

                    if display:
                        disp.displayGrid(grid, x, y, hideNumbers=displayHideNumbers, default=default, message=message)
                    
                    grid[y][x] = 0 # reset square
                
                return False # attempts failed, backtrack

    return grid


# backtracking (should call it like that)
def randomSolve(grid, display=False, shufflePossible=False, displayHideNumbers=False, default=None, message=""):
    if default == None:
        default = copy.deepcopy(grid)

    solved = False

    while not solved:
        solved = True

        for x in range(0,9):
            for y in range(0,9):
                # find empty square
                if grid[y][x] == 0 and default[y][x] == 0:
                    grid[y][x] = random.randint(1, 9) # try random solution

                    if display:
                        disp.displayGrid(grid, x, y, hideNumbers=displayHideNumbers, default=default, message=message)
        
        erros = []

        for x in range(0, 9):
            for y in range(0, 9):
                if default[y][x] == 0 and not possible(grid, x, y, grid[y][x]):
                    solved = False
                    erros.append((x, y))


        while len(erros) > 0:
            x, y = erros.pop()
            grid[y][x] = 0

            if display:
                disp.displayGrid(grid, x, y, hideNumbers=displayHideNumbers, default=default, message=message)

    return grid


# uses backtracking but tries the squares with the least possible solutions first
def lessPossibilitiesFirstSolver(grid, display=False, shufflePossible=False, displayHideNumbers=False, default=None, message=""): 
    emptySquares = dict()
    solved = True

    selectedSquare = (-1, -1, [i for i in range(1, 10)])

    for x in range(9):
        for y in range(9):
            if grid[y][x] == 0:
                solved = False

                possibleSolutions = [n for n in range(1, 10) if possible(grid, x, y, n)] # find possible solutions

                # if len is 0 we need to backtrack
                if len(possibleSolutions) == 0:
                    grid[y][x] = 0
                    return False

                if len(possibleSolutions) <= len(selectedSquare[2]):
                    selectedSquare = (x, y, possibleSolutions)

                if len(possibleSolutions) < 1:
                    break

    x, y, possibleSolutions = selectedSquare

    if solved:
        return grid

    if shufflePossible:
        random.shuffle(possibleSolutions)

    for attempt in possibleSolutions:
        grid[y][x] = attempt # try solution
    
    if display:
        disp.displayGrid(grid, x, y, hideNumbers=displayHideNumbers, default=default, message=message)

    if lessPossibilitiesFirstSolver(grid, display=display, shufflePossible=shufflePossible, displayHideNumbers=displayHideNumbers, default=default, message=message): 
        return grid # solution found
    else:
        grid[y][x] = 0
        return False


# generate a random grid with a given number of clues
# useSolveAfter: after a given number of randomly placed numbers the grid will be solved
#                to ensure that the grid is solvable if it isnt the function will be called again
# using a low number in useSolveAfter will result in a less randomized grid
# using a high number in useSolveAfter will result in more failed attempts thus a slower runtime
def randomGrid(clues, useSolveAfter=10, display=False, solveAlgo=solve):
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
    
    grid = solveAlgo(grid, display=display, shufflePossible=True, displayHideNumbers=True, default=False, message="Generating...") # solve grid

    if grid == False:
        grid = randomGrid(clues, useSolveAfter)


    removeNums = [(x, y) for x in range(0, 9) for y in range(0, 9)] # list of positions to remove numbers from
    random.shuffle(removeNums) # shuffle list

    removeNums = removeNums[: 81 - clues] # get first n positions 

    for x, y in removeNums:
        grid[y][x] = 0

    return grid


def compare(strategies, grids, display=False):
    times = {strategy.__name__: [] for strategy in strategies}

    for i in range(grids):
        print(i,"/",grids)
        clues = i % 81
        grid = randomGrid(clues, display=display, solveAlgo=lessPossibilitiesFirstSolver)

        for strategy in strategies:
            grid_copy = copy.deepcopy(grid)
            
            start = time.time()
            grid_copy = strategy(grid_copy, display=display, shufflePossible=False, displayHideNumbers=False, default=grid, message= str(i) +  strategy.__name__ + "Solving...")
            end = time.time()

            times[strategy.__name__].append(end - start)

    averages = {strategy: sum(times[strategy]) / len(times[strategy]) for strategy in times}

    return times, averages


def main():
    if "-h" in sys.argv:
        print("Usage: python3 solver.py [option]")
        print("Options:")
        print("   -r: generate random grid [number of clues]")
        print("   -s: solve a grid")
        print("   --repeat: dont stop after solving a grid")
        print("   --no-input: dont wait for input after solving a grid")
        print("   --strategy: choose between backtracking, lpf and random")
        print("   -c: compare different strategies [number of grids [strategy1] [strategy2] [strategy3] ...]")
        print("   -h: display this message")
        exit()

    
    strategy = solve
    genratorSolve = solve


    # clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')


    grid = defaultGrid

    if "-r" in sys.argv:
        clues = 50

        if len(sys.argv) > 2 and sys.argv[2].isdigit():
            clues = sys.argv[2]
    
        grid = randomGrid(int(clues), display=True)


    grid_before_solve = copy.deepcopy(grid)

    if "-c" in sys.argv:
        strategies = []

        for arg in sys.argv[sys.argv.index("-c") + 2:]:
            if arg == "random":
                strategies.append(randomSolve)
            elif arg == "lpf":
                strategies.append(lessPossibilitiesFirstSolver)
            elif arg == "backtracking":
                strategies.append(solve)

        times, averages = compare(strategies, int(sys.argv[sys.argv.index("-c") + 1]), display=False)

        print("Strategy\t\tAverage time")
        for strategy in strategies:
            print(strategy.__name__ + "\t\t" + str(averages[strategy.__name__]))

        print("best: " + min(averages, key=averages.get))

        exit()


    if "--strategy" in sys.argv:
        if sys.argv[sys.argv.index("--strategy") + 1] == "random":
            strategy = randomSolve
        elif sys.argv[sys.argv.index("--strategy") + 1] == "lpf":
            strategy = lessPossibilitiesFirstSolver


    if "-s" in sys.argv:
        grid = strategy(grid, display=True, shufflePossible=False, displayHideNumbers=False, default=grid_before_solve, message="Solving...")
    
    
    disp.displayGrid(grid, -1, -1, hideNumbers=False, default=grid_before_solve, message="Done")

    if "--no-input" not in sys.argv:
        input("Press enter to exit")
    

    if "--repeat" in sys.argv:
        main()
    exit()


if __name__ == "__main__":
    main()