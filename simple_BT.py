import copy
import math
from typing import List

from cell import Cell
from hidden_pairs import HiddenPairs
from hidden_singles import HiddenSingles
from hidden_triples import HiddenTriples
from inference import InferenceRule
from most_constrained import is_valid_cell_value
from naked_pairs import NakedPairs
from naked_singles import NakedSingles
from naked_triples import NakedTriples
from sudoku import Sudoku
# import sudoku

from queue import PriorityQueue


# q = PriorityQueue()
#
# q.put((4, 'Read'))
# q.put((2, 'Play'))
# q.put((5, 'Write'))
# q.put((1, 'Code'))
# q.put((3, 'Study'))
#
# while not q.empty():
#     next_item = q.get()
#     print(next_item)


def find_next_cell(i, j):
    # if j is not the last col
    if j <= 7:
        return i, j + 1
    else:
        if i <= 7:
            return i + 1, 0
        else:
            return None


def solve_simple_BT(sudoku: Sudoku, history: List, rules: List[InferenceRule], cell):
    if sudoku.is_board_solved():
        return sudoku

    for rule in rules:
        rule_obj = rule(sudoku)
        try:
            rule_obj.evaluate()
        except Exception as e:
            return -1
        # rule_obj.evaluate()

        sudoku = rule_obj.puzzle
        if sudoku.is_board_solved():
            return sudoku

    i, j = cell
    possible_values = sudoku.board[i][j]
    next_cell = find_next_cell(i, j)

    # print(f'{history}')
    # print(f'{i}, {j}, {possible_values}')

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

            if next_cell is not None:
                possible_sudoku = solve_simple_BT(new_sudoku, history + [((i, j), val)], rules, next_cell)
                if possible_sudoku != -1:
                    return possible_sudoku
            else:
                # this turn is the last cell
                return new_sudoku.is_board_solved()

    return -1
    # print(f'out of values for {i}, {j}')
    # raise Exception('Cannnot solve')
    # return -1


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
    # puzzle_2_medium = '''020 004 000
    # 003 000 204
    # 140 080 503
    # 030 802 000
    # 200 000 006
    # 000 409 050
    # 402 070 081
    # 807 000 600
    # 000 600 070
    # '''

    sudoku = Sudoku(EVIL_SUDOKU)
    # rules = [NakedSingles, HiddenSingles, NakedPairs, HiddenPairs, NakedTriples]
    rules = [HiddenTriples]
    # rules = []
    # rules = [NakedSingles, HiddenSingles, NakedPairs, HiddenPairs, NakedTriples]

    solved_sudoku = solve_simple_BT(sudoku, [], rules, (0, 0))
    # assert solved_sudoku.is_board_solved()
    if solved_sudoku != -1:
        solved_sudoku.print()
    else:
        print('error')


def test_most_constrained_self():
    sudoku = Sudoku(EVIL_SUDOKU)
    print(sudoku.solve_most_constrained_var())
    sudoku.print()


if __name__ == '__main__':
    # test_most_constrained_self()
    test_most_constrained_func()
    # print(find_next_cell(8, 1))
