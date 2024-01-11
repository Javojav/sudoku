import solver
import display as disp
import re
import os 
import copy

def startGame():
    os.system('cls' if os.name == 'nt' else 'clear')

    clues = input("Enter how many clues you want: ")

    if not clues:
        return startGame()
    else:
        clues = int(clues)

    if clues > 81:
        clues = 81

    grid = solver.randomGrid(clues)
    disp.displayGrid(grid, 0, 0, hideNumbers=False, default=grid)

    return grid


def checkWin(grid):
    for i in range(0, 9):
        for j in range(0, 9):
            if grid[i][j] == 0 or solver.possible(grid, j, i, grid[i][j]) == False:
                return False
    
    return True


def getInput():
    move = None
    num = None
    position = None
    solve = False
    check = False

    inputChar = input("Enter a number, direction (x, y), move w/a/s/d, x to getSolution, c to check,  or quit q: ")

    if not inputChar:
        return move, num, position

    # direction
    if re.match(r'\d,\d', inputChar):
        position = [int(n) - 1 for n in inputChar.split(',')] 
        if position[0] > 8 or position[1] > 8 or position[0] < 0 or position[1] < 0: # check if position is valid
            return move, num, None, solve, check

    if inputChar == 'w':
        move = 'Up'
    elif inputChar == 'a':
        move = 'Left'
    elif inputChar == 's':
        move = 'Down'
    elif inputChar == 'd':
        move = 'Right'
    elif inputChar in '123456789':
        num = int(inputChar)
    elif inputChar == 'q':
        exit()
    elif inputChar == "c":
        check = True
    elif inputChar == "x":
        solve = True

    return move, num, position, solve, check


def moveCursor(dir, position, defaultGrid):
    if dir == 'Up':
        position[1] = position[1] - 1 if position[1] != 0 else 8
    elif dir == 'Down':
        position[1] = (position[1] + 1) % 8
    elif dir == 'Left':
        position[0] = position[0] - 1 if position[0] != 0 else 8
    elif dir == 'Right':
        position[0] = (position[0] + 1) % 8
    
    if defaultGrid[position[1]][position[0]] != 0:
        moveCursor(dir, position, defaultGrid) # if the cursor is on a default number, move it again

    return position


def gameControl():
    over = False
    position = [0, 0]

    startGrid = startGame()
    
    grid = copy.deepcopy(startGrid)
    
    while not over:
        move, num, pos, solve, check = getInput()

        if move:
            position = moveCursor(move, position, startGrid)
        
        if pos:
            position = pos

        x, y = position

        if num and startGrid[y][x] == 0: 
            grid[y][x] = num
        
        if solve:
            solver.solve(grid, display=True, shufflePossible=True, displayHideNumbers=True)
        
        if check:
            if checkWin(grid):
                print("You win!")
                over = True
            else:
                print("Not right")
                
            
        disp.displayGrid(grid, x, y, hideNumbers=False, default=startGrid)


if __name__ == "__main__":
    gameControl()