#!/usr/bin/python3

import unittest
from collections import defaultdict

from cell import Cell
from inference import InferenceRule

class HiddenPairs(InferenceRule):
    def evaluate(self):
        """
        http://sudokuessentials.com/sudoku_tips/
        In the example at the left there is a hidden pair 2 and 9.
        They are circled in red. Hidden pairs are identified by the fact that a pair of
        numbers occur in only two cells of a row, column, or region.
        They are “hidden” because the other numbers in the two cells make their presence harder to spot.

        It is safe to remove all other digits from the two cells circled in red so that only the two and nine remain.
        Hidden pairs will appear often in your Sudoku puzzles and games.See link above for example.
        """
        cell_changed = True  # run init at least once
        while cell_changed:  # keep running when a change is made
            cell_changed = False  # this ensures a change is made every loop

            # check rows
            for row in range(9):
                cells = self.puzzle.get_row(row)
                matches = self.evaluate_group(cells)
                if self.execute_group(matches):
                    self.move_count += 1
                    cell_changed = True
                    self.puzzle.is_board_valid()

            # search cols
            for col in range(9):
                cells = self.puzzle.get_col(col)
                matches = self.evaluate_group(cells)
                if self.execute_group(matches):
                    self.move_count += 1
                    cell_changed = True
                    self.puzzle.is_board_valid()

            # search regions
            for reg in range(9):
                cells = self.puzzle.get_region(reg)
                matches = self.evaluate_group(cells)
                if self.execute_group(matches):
                    self.move_count += 1
                    cell_changed = True
                    self.puzzle.is_board_valid()


    @staticmethod
    def evaluate_group(cells):
        """
        Given a list of cells, find hidden pairs
        """

        # maintain a dictionary of possible values
        # key = value (1-9), value = list of cells where it could be
        poss_values = defaultdict(list)
        for cell in cells:
            for val in cell.val:
                poss_values[val].append(Cell(cell.row, cell.col, []))       # note the empty value, we only care about cell position

        # if there are exactly two keys that are in the same two cells, those are a hidden pair
        pairs = []
        for val in poss_values:
            if len(poss_values[val]) == 2:
                pairs.append(val)

        # there can only be two values for a pair
        if len(pairs) != 2:
            return []

        # if the two values share the same two cells
        # every other possible value in those two cells can be removed (this needs to be done by CALLER)
        if poss_values[pairs[0]] == poss_values[pairs[1]]:
            matches = []
            for cell in poss_values[pairs[0]]:
                matches.append(Cell(cell.row, cell.col, pairs))
            return matches

        # else no match
        return []

    def execute_group(self, matches):
        """
        Given 2 matching cells whose values contain a hidden pair, remove all other values from the paired cells
        If the paired cells both already contain only the two numbers, return False (nothing was done)
        """
        if not matches:
            return False

        cell0 = matches[0]              # local var for readability (no extra brackets)
        cell1 = matches[1]
        if self.puzzle.board[cell0.row][cell0.col] == self.puzzle.board[cell1.row][cell1.col]:      # the cells already only contain the two numbers, nothing to do
            return False

        # debug print statements
        # print(f'Matches {matches[0]} {matches[1]}')
        # print(f'Values  {self.puzzle.board[cell0.row][cell0.col]} {self.puzzle.board[cell1.row][cell1.col]}')
        # print(f'Board before')
        # self.puzzle.print(simple=False)

        # update the board
        self.puzzle.board[cell0.row][cell0.col] = list(cell0.val)
        self.puzzle.board[cell1.row][cell1.col] = list(cell1.val)

        # print(f'After before')
        # self.puzzle.print(simple=False)

        return True                     # let caller know we took an action


class TestHiddenPairs(unittest.TestCase):
    def test_evaluate_group(self):
        """
        See example from link above
        """
        cells = [
            Cell(0, 0, [8]),
            Cell(0, 1, [1, 7]),
            Cell(0, 2, [2, 7, 9]),              # hidden 2 and 9 pair
            Cell(0, 3, [3, 4, 5, 7]),
            Cell(0, 4, [3, 4, 5, 7]),
            Cell(0, 5, [3, 4, 7]),
            Cell(0, 6, [1, 2, 3, 5, 9]),        # hidden 2 and 9 pair
            Cell(0, 7, [1, 3, 5]),
            Cell(0, 8, [6])
        ]

        expected = [
            Cell(0, 2, [2, 9]),
            Cell(0, 6, [2, 9])
        ]

        # this verifies the match, the caller should remove every value OTHER than 2 and 9 at cells 0,2 and 0,6

        actual = HiddenPairs.evaluate_group(cells)
        self.assertEqual(expected, actual)

    def test_evaluate_group_no_matches(self):
        """
        Same as the previous test but 2 is added to cell 0,3.
        This makes 2 and 9 no longer a hidden pair, no matches should be found
        """
        cells = [
            Cell(0, 0, [8]),
            Cell(0, 1, [1, 7]),
            Cell(0, 2, [2, 7, 9]),              # hidden 2 and 9 NOT a pair
            Cell(0, 3, [2, 3, 4, 5, 7]),        # 2 in this cell invalidates the pair
            Cell(0, 4, [3, 4, 5, 7]),
            Cell(0, 5, [3, 4, 7]),
            Cell(0, 6, [1, 2, 3, 5, 9]),        # hidden 2 and 9 NOT a pair
            Cell(0, 7, [1, 3, 5]),
            Cell(0, 8, [6])
        ]

        expected = []

        # this verifies the match, the caller should remove every value OTHER than 2 and 9 at cells 0,2 and 0,6

        actual = HiddenPairs.evaluate_group(cells)
        self.assertEqual(expected, actual)

    def test_full_puzzle(self):
        """
        Integration test using a full puzzle string and validate match found
        """
        from data_collection import SudokuDataCollection
        dc = SudokuDataCollection()
        dc.load_puzzles()
        (ns, hs, np, hp, nt, ht) = dc.run_single_test('60 Evil', 2)

        self.assertEqual(1, hp, 'This puzzle contains 1 known hidden pair at start')


if __name__ == '__main__':
    unittest.main()
