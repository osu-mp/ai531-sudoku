import copy
import math
from typing import List

from cell import Cell
from sudoku import Sudoku

from queue import PriorityQueue

q = PriorityQueue()

q.put((4, 'Read'))
q.put((2, 'Play'))
q.put((5, 'Write'))
q.put((1, 'Code'))
q.put((3, 'Study'))

while not q.empty():
    next_item = q.get()
    print(next_item)


def get_sorted_constrained_vars(sudoku: Sudoku):
    # res = PriorityQueue()
    res = []
    for i in range(9):
        for j in range(9):
            if len(sudoku.board[i][j]) > 1:
                res.append((len(sudoku.board[i][j]), (i, j)))
    res.sort()
    return res


def is_final_cell(board_vals: List[int]):
    return len(board_vals) == 1


def is_conflict_other_cell(val, vals_other_cell):
    return val in vals_other_cell and is_final_cell(vals_other_cell)


def is_valid_cell_value(val, board, row, col):
    """
    Checks 3 is value is possible or not with 3 conditions:
    1. Check repetition in column
    2. Check repetition in row
    3. Check repetition in 3x3 grid
def solve_fixed_baseline_backtrack(self, start_row=0, start_col=0, count=0):
    """
    # Checks for repeated values in column

    for col_counter in range(0, 9):
        if is_conflict_other_cell(val, board[row][col_counter]):
            return False

    # Checks for repeated values in row
    for row_counter in range(0, 9):
        if is_conflict_other_cell(val, board[row_counter][col]):
            return False

    # Checks for repeated values in 3x3 grid
    row_for_small_grid = math.floor(row / 3) * 3
    col_for_small_grid = math.floor(col / 3) * 3
    for miniRow in range(0, 3):
        for miniCol in range(0, 3):
            if is_conflict_other_cell(val, board[row_for_small_grid + miniRow][col_for_small_grid + miniCol]):
                return False

    return True


def solve_most_constrained_var(sudoku: Sudoku, history: List):
    """
    Most Constrained Variable: Pick a slot that has the least number of values in its domain.
    """
    # TODO get most constrained variable
    # sudoku = copy.deepcopy(sudoku)

    if sudoku.is_board_solved():
        return sudoku

    queue_cells = get_sorted_constrained_vars(sudoku)
    if len(queue_cells) == 0:
        print('solved')
        sudoku.print()
        return sudoku

    for q_item in queue_cells:
        i, j = q_item[1]
        possible_values = sudoku.board[i][j]

        for val in possible_values:
            if is_valid_cell_value(val, sudoku.board, i, j):
                print(f'BT {i}, {j}, val = {val}')
                new_sudoku = copy.deepcopy(sudoku)
                new_sudoku.board[i][j] = [val]

                # update val of all other cells
                new_sudoku.solve_cell(Cell(i, j, val))
                possible_sudoku = solve_most_constrained_var(new_sudoku, history + [((i, j), val)])

                if possible_sudoku != -1:
                    return possible_sudoku

        print(f'out of values for {i}, {j}')
        return -1

    return -1
    # return sudoku


if __name__ == '__main__':
    puzzle_2_medium = '''020 004 000
    003 000 204
    140 080 503
    030 802 000
    200 000 006
    000 409 050
    402 070 081
    807 000 600
    000 600 070
    '''
    sudoku = Sudoku(puzzle_2_medium)
    print(solve_most_constrained_var(sudoku, []))
