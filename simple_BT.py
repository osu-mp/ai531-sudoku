import copy
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


def find_next_cell(i, j):
    # if j is not the last col
    if j <= 7:
        return i, j + 1
    else:
        if i <= 7:
            return i + 1, 0
        else:
            return None


class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def __repr__(self):
        return str(self.value)


# counter = Counter()
# counter = 0
# from utility import counter
import utility


def solve_simple_BT(sudoku: Sudoku, rules: List[InferenceRule] = [], cell=(0, 0)):
    # if sudoku.is_board_solved():
    #     return sudoku
    utility.counter += 1

    for rule in rules:
        if isinstance(rule, InferenceRule):
            rule_obj = rule
        else:
            rule_obj = rule(sudoku)

            # if isinstance(rule_obj, )
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
                possible_sudoku = solve_simple_BT(new_sudoku, rules, next_cell)

                if possible_sudoku != -1:
                    return possible_sudoku
            else:
                # this turn is the last cell
                if new_sudoku.is_board_solved():
                    return new_sudoku

    return -1


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

EASY_SUDOKU = '''240 300 000
000 520 407
000 046 008
610 700 084
009 060 500
730 005 061
100 470 000
302 051 000
000 002 019'''


def test_simple_BT_func():
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

    # sudoku = Sudoku(EASY_SUDOKU)
    sudoku = Sudoku(EVIL_SUDOKU)
    # rules = [NakedSingles(sudoku), HiddenSingles(sudoku), NakedPairs(sudoku), HiddenPairs(sudoku), NakedTriples(sudoku)]
    # rules = [HiddenTriples(sudoku)]
    rules = [NakedSingles, HiddenSingles, NakedPairs, HiddenPairs, NakedTriples]
    # rules = []

    utility.counter = 0
    solved_sudoku = solve_simple_BT(sudoku, rules, (0, 0))
    print(f'{solved_sudoku=}')
    print(f'{utility.counter=}')
    print(rules)
    # print([rule.move_count for rule in rules])


if __name__ == '__main__':
    # test_most_constrained_self()
    test_simple_BT_func()
    # print(find_next_cell(8, 1))
