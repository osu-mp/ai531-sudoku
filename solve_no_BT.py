from typing import List

import utility
from hidden_pairs import HiddenPairs
from hidden_singles import HiddenSingles
from hidden_triples import HiddenTriples
from inference import InferenceRule
from naked_pairs import NakedPairs
from naked_singles import NakedSingles
from naked_triples import NakedTriples
from sudoku import Sudoku


def solve_no_BT(sudoku: Sudoku, rules: List[InferenceRule] = []):
    utility.counter += 1
    MAX_LOOP = 1000

    for loop in range(MAX_LOOP):
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

            if isinstance(rule_obj, NakedSingles):
                utility.rule_tracker.naked_singles += rule_obj.move_count
            elif isinstance(rule_obj, HiddenSingles):
                utility.rule_tracker.hidden_singles += rule_obj.move_count
            elif isinstance(rule_obj, NakedPairs):
                utility.rule_tracker.naked_pairs += rule_obj.move_count
            elif isinstance(rule_obj, HiddenPairs):
                utility.rule_tracker.hidden_pairs += rule_obj.move_count
            elif isinstance(rule_obj, NakedTriples):
                utility.rule_tracker.naked_triples += rule_obj.move_count
            elif isinstance(rule_obj, HiddenTriples):
                utility.rule_tracker.hidden_triples += rule_obj.move_count

            sudoku = rule_obj.puzzle
            if sudoku.is_board_solved():
                return sudoku

    return None


if __name__ == '__main__':

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
    rules = [NakedSingles, HiddenSingles, NakedPairs, HiddenPairs, NakedTriples, HiddenTriples]
    sudoku = solve_no_BT(Sudoku(EVIL_SUDOKU), rules)
    sudoku.print()
