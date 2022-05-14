import copy
import math
from typing import List

import utility
from cell import Cell
from hidden_pairs import HiddenPairs
from hidden_singles import HiddenSingles
from hidden_triples import HiddenTriples
from inference import InferenceRule
from naked_pairs import NakedPairs
from naked_singles import NakedSingles
from naked_triples import NakedTriples
from sudoku import Sudoku


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
        if col_counter != col:
            if is_conflict_other_cell(val, board[row][col_counter]):
                return False

    # Checks for repeated values in row
    for row_counter in range(0, 9):
        if row_counter != row:
            if is_conflict_other_cell(val, board[row_counter][col]):
                return False

    # Checks for repeated values in 3x3 grid
    row_for_small_grid = math.floor(row / 3) * 3
    col_for_small_grid = math.floor(col / 3) * 3
    for miniRow in range(0, 3):
        for miniCol in range(0, 3):
            row_mini = row_for_small_grid + miniRow
            col_mini = col_for_small_grid + miniCol
            if row_mini != row and col_mini != col:
                if is_conflict_other_cell(val, board[row_mini][col_mini]):
                    return False
    return True


def solve_most_constrained_var(sudoku: Sudoku, rules: List[InferenceRule] = []):
    """
    Most Constrained Variable: Pick a slot that has the least number of values in its domain.
    """
    # if sudoku.is_board_solved():
    #     return sudoku
    utility.counter += 1
    for rule in rules:
        if isinstance(rule, InferenceRule):
            rule_obj = rule
        else:
            rule_obj = rule(sudoku)
        try:
            rule_obj.evaluate()
        except Exception as e:
            return -1
        # rule_obj.evaluate()

        sudoku = rule_obj.puzzle
        if sudoku.is_board_solved():
            return sudoku

    queue_cells = get_sorted_constrained_vars(sudoku)
    if len(queue_cells) == 0:
        # print('solved')
        # sudoku.print()
        return sudoku

    for q_item in queue_cells:
        i, j = q_item[1]
        possible_values = sudoku.board[i][j]

        for val in possible_values:
            if is_valid_cell_value(val, sudoku.board, i, j):
                # print(f'BT {i}, {j}, val = {val}')
                new_sudoku = copy.deepcopy(sudoku)
                new_sudoku.board[i][j] = [val]
                # update val of all other cells
                try:
                    new_sudoku.solve_cell(Cell(i, j, val))
                except Exception as e:
                    # print('Error = ', e)
                    continue

                possible_sudoku = solve_most_constrained_var(new_sudoku, rules)
                if possible_sudoku != -1:
                    return possible_sudoku

        # print(f'out of values for {i}, {j}')
        return -1

    return -1
    # return sudoku


EVIL_SUDOKU = '''000 006 009
090 300 108
076 000 402
000 800 005
000 502 000
900 003 000
409 000 830
605 004 090
700 100 000
'''


def test_most_constrained_func():
    sudoku = Sudoku(EVIL_SUDOKU)
    # rules = [NakedSingles(sudoku), HiddenSingles(sudoku), NakedPairs(sudoku), HiddenPairs(sudoku), NakedTriples(sudoku)]
    # rules = [NakedSingles(sudoku), HiddenSingles(sudoku)]
    rules = [HiddenTriples]
    # rules = []
    utility.counter = 0
    solved_sudoku = solve_most_constrained_var(sudoku, rules)
    # assert solved_sudoku.is_board_solved()
    if solved_sudoku != -1:
        solved_sudoku.print()
        print(utility.counter)
    else:
        print('error')


def test_most_constrained_self():
    sudoku = Sudoku(EVIL_SUDOKU)
    # print(sudoku.solve_most_constrained_var())
    sudoku.print()


if __name__ == '__main__':
    # test_most_constrained_self()
    test_most_constrained_func()
