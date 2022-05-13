
puzzle = [
[0, 0, 2, 0, 9, 0, 6, 0, 0],
[6, 0, 9, 0, 0, 0, 0, 0, 0],
[4, 8, 0, 0, 0, 6, 0, 0, 0],
[0, 0, 8, 4, 0, 2, 0, 9, 0],
[3, 0, 0, 0, 0, 0, 0, 0, 7],
[0, 7, 0, 3, 0, 9, 1, 0, 0],
[0, 0, 0, 6, 0, 0, 0, 5, 1],
[0, 0, 0, 0, 0, 0, 2, 0, 4],
[0, 0, 7, 0, 8, 0, 3, 0, 0]

]
"""
puzzle =    [
[8, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 3, 6, 0, 0, 0, 0, 0],
[0, 7, 0, 0, 9, 0, 2, 0, 0],
[0, 5, 0, 0, 0, 7, 0, 0, 0],
[0, 0, 0, 0, 4, 5, 7, 0, 0],
[0, 0, 0, 1, 0, 0, 0, 3, 0],
[0, 0, 1, 0, 0, 0, 0, 6, 8],
[0, 0, 8, 5, 0, 0, 0, 1, 0],
[0, 9, 0, 0, 0, 0, 4, 0, 0]
]
"""
import math



def printBoard(board):
    for i in range(0, 9):
        for j in range(0, 9):
            print(board[i][j], end=" ")
        print()

def is_valid(digit, board, row, col):
    """
    Checks 3 is value is possible or not with 3 conditions:
    1. Check repetation in column
    2. Check repetation in row
    3. Check repetation in 3x3 grid

    """
    # Checks for repeated values in column
    for col_counter in range(0,9):
        if board[row][col_counter] == digit:
            return False

    # Checks for repeated values in row
    for row_counter in range(0,9):
        if board[row_counter][col] == digit:
            return False

    # Checks for repeated values in 3x3 grid
    row_for_small_grid = math.floor(row / 3) * 3
    col_for_small_grid = math.floor(col / 3) * 3
    for miniRow in range(0,3):
        for miniCol in range(0,3):
            if board[row_for_small_grid + miniRow][col_for_small_grid + miniCol] == digit:
                return False

    return True


def solve_fixed_baseline_backtrack(bt_count):
    
    for row in range(0, 9):
        for col in range(0, 9):
            if puzzle[row][col] == 0:

                for digit in range(1, 10):
                    if is_valid(digit, puzzle, row, col):
                        puzzle[row][col] = digit
                        solve_fixed_baseline_backtrack(bt_count)
                        bt_count = bt_count + 1
                        puzzle[row][col] = 0
                    
                return 
    print(bt_count)             
    printBoard(puzzle)               
    
    
    

ans = solve_fixed_baseline_backtrack(0)
