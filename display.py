import sys

def displayGrid(grid, x=-1, y=-1, hideNumbers=False, default=False, message=""):
    sys.stdout.write("\033[H") # move cursor to top left
    for i in range(0, 9):
        for j in range(0, 9):
            char = 'X' if hideNumbers else str(grid[i][j])
            char = char if grid[i][j] != 0 else "_"

            if i == y and j == x:
                sys.stdout.write("\033[1;31m" + char + "\033[0m ")
            elif default and default[i][j] != 0:
                sys.stdout.write("\033[1;32m" + char + "\033[0m ")
            else:
                sys.stdout.write(char + " ")
        sys.stdout.write("\n")
    sys.stdout.write(" " * 90)# clear line
    sys.stdout.write("\033[L") # move cursor to left
    sys.stdout.write(message)
    sys.stdout.write("\n")

  
    sys.stdout.flush()