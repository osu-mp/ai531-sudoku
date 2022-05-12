#!/usr/bin/python3

import itertools
import unittest
from collections import defaultdict

from cell import Cell
from inference import InferenceRule

class NakedTriples(InferenceRule):
    def evaluate(self):
        """
        http://sudokuessentials.com/sudoku_tips/
        Another Sudoku tip is to look for “naked triples”.
        Naked triples like the name suggests are three numbers that do not have any other
        numbers residing in the cells with them.

        Unlike naked pairs, naked triples do not need all of the three candidates in every cell.
        Quite often only two of the three candidates will be shown.

        In the example at the left, the three cells circled are the three naked triples.
        They are 5,6 and 9. Only a 5,6 and 9 can appear in those three locations.
        Therefore, you can remove all 5,6, and 9s from the other cells in this row.

        When you remove the 6,9 from two cells and the 5,6 you will discover a naked pair (1,4)
        and a hidden single (2). See how these Sudoku tips help you solve puzzles?
        See link above for example.
        """
        cell_changed = True  # run init at least once
        while cell_changed:  # keep running when a change is made
            cell_changed = False  # this ensures a change is made every loop

            # check rows
            for row in range(9):
                cells = self.puzzle.get_row(row)
                matches, triples = self.evaluate_group(cells)
                if self.execute_group(matches, cells, triples):
                    self.move_count += 1
                    cell_changed = True
                    self.puzzle.is_board_valid()

            # check cols
            for col in range(9):
                cells = self.puzzle.get_col(col)
                matches, triples = self.evaluate_group(cells)
                if self.execute_group(matches, cells, triples):
                    self.move_count += 1
                    cell_changed = True
                    self.puzzle.is_board_valid()

            # check regions
            for reg in range(9):
                cells = self.puzzle.get_region(reg)
                matches, triples = self.evaluate_group(cells)
                if self.execute_group(matches, cells, triples):
                    self.move_count += 1
                    cell_changed = True
                    self.puzzle.is_board_valid()

    @staticmethod
    def evaluate_group(cells):
        """
        Given a list of cells, find naked triples
        """

        # only cells that have 2 or 3 possible values are candidates for triples, so prune all others
        triple_cells = defaultdict(list)            # dictionary of candidates
        poss_triples = set()                        # set of numbers in those candidates
        for cell in cells:
            values = cell.val
            if len(values) == 1 or len(values) > 3:  # ignore every cell with more than 3 possible values
                continue

            key = str(values)
            for val in values:
                poss_triples.add(val)
            triple_cells[key].append(Cell(cell.row, cell.col, values))

        # generate all possible combinations of 2 and 3 from the candidate numbers
        combos2 = list(itertools.combinations(poss_triples, 2))
        combos3 = list(itertools.combinations(poss_triples, 3))

        # save any of these combos that were found in the cells
        found_combos = []
        for combo in combos3 + combos2:
            if str(list(sorted(combo))) in triple_cells.keys():
                found_combos.append(combo)

        # for the final check, each individual value must appear in 2 or 3 cells to be a candidate triple
        # so discard any number that is only in one cell
        final_trips = set()
        for value in poss_triples:
            found_count = 0
            for combo in found_combos:
                if value in combo:
                    found_count += 1
            if found_count > 1:
                final_trips.add(value)

        # save the 3 cells that matched
        matches = []
        for cell in cells:
            values = cell.val
            if len(values) == 1 or len(values) > 3:  # ignore every cell with more than 3 possible values
                continue

            if set(values).issubset(final_trips):
                matches.append(cell)

        # error checking: if the triple is not actually a triple, do not return anything
        if len(final_trips) != 3:
            return [], set()
        if len(matches) != 0 and len(matches) != 3:
            return [], set()

        return matches, final_trips

    def execute_group(self, matches, cells, triple_values):
        if not matches:
            return False

        value_removed = False
        for cell in cells:
            # print(f'{cell}  triples={triple_values}')
            if cell in matches:
                continue
            for value in cell.val:
                if value in triple_values:
                    self.puzzle.board[cell.row][cell.col].remove(value)
                    value_removed = True

        return value_removed


class TestNakedTriples(unittest.TestCase):
    def test_evaluate_group(self):
        cells = [
            Cell(0, 0, [3]),
            Cell(0, 1, [5, 6]),             # naked triple
            Cell(0, 2, [1, 4, 6, 9]),
            Cell(0, 3, [7]),
            Cell(0, 4, [6, 9]),             # naked triple
            Cell(0, 5, [2, 4, 5, 6]),
            Cell(0, 6, [8]),
            Cell(0, 7, [5, 9]),             # naked triple
            Cell(0, 8, [1, 4, 6, 9])
        ]

        expected_cells = [
            Cell(0, 1, [5, 6]),
            Cell(0, 4, [6, 9]),
            Cell(0, 7, [5, 9])
        ]
        expected_triples = set([5, 6, 9])

        actual_cells, actual_triples = NakedTriples.evaluate_group(cells)
        self.assertEqual(expected_cells, actual_cells)
        self.assertEqual(expected_triples, actual_triples)

    def test_evaluate_group_case2(self):
        cells = [
            Cell(0, 0, [7, 8, 9]),      # naked triple
            Cell(0, 1, [1]),
            Cell(0, 2, [7, 8]),         # naked triple
            Cell(0, 3, [3, 5, 9]),
            Cell(0, 4, [4]),
            Cell(0, 5, [5, 6, 8, 9]),
            Cell(0, 6, [7, 9]),         # naked triple
            Cell(0, 7, [2]),
            Cell(0, 8, [3, 5, 6, 7, 8, 9])
        ]

        expected_cells = [
            Cell(0, 0, [7, 8, 9]),
            Cell(0, 2, [7, 8]),
            Cell(0, 6, [7, 9])
        ]
        expected_triples = set([7, 8, 9])

        actual_cells, actual_triples = NakedTriples.evaluate_group(cells)
        self.assertEqual(expected_cells, actual_cells)
        self.assertEqual(expected_triples, actual_triples)



if __name__ == '__main__':
    unittest.main()
