#!/usr/bin/python3

import unittest
from collections import defaultdict

from cell import Cell
from inference import InferenceRule

class NakedPairs(InferenceRule):
    def evaluate(self):
        """
        http://sudokuessentials.com/sudoku_tips/
        In the example to the left there is a “naked pair”.
        A naked pair is two identical candidates in a particular row, column, or region.
        This combination of candidates will occur often also.

        When you see a naked pair, it is safe to eliminate those two numbers from all other cells
        in the row, column, or region the pair reside in.

        In the naked pair example, it is safe to eliminate the four and six from the two quads of 3,4,6, and 8.
        Doing so, leaves two 3,8 pairs. The 3,4,6, and 8 quads are really “hidden pairs”. More Sudoku tips on this.
        See link above for example.
        """
        cell_changed = True  # run init at least once
        while cell_changed:  # keep running when a change is made
            cell_changed = False  # this ensures a change is made every loop

            # check rows
            for row in range(9):
                cells = self.puzzle.get_row(row)
                matches = self.evaluate_group(cells)
                if self.execute_group(matches, cells):
                    self.move_count += 1
                    cell_changed = True
                    self.puzzle.is_board_valid()

            # check cols
            for col in range(9):
                cells = self.puzzle.get_col(col)
                matches = self.evaluate_group(cells)
                if self.execute_group(matches, cells):
                    self.move_count += 1
                    cell_changed = True
                    self.puzzle.is_board_valid()

            # check regions
            for reg in range(9):
                cells = self.puzzle.get_region(reg)
                matches = self.evaluate_group(cells)
                if self.execute_group(matches, cells):
                    self.move_count += 1
                    cell_changed = True
                    self.puzzle.is_board_valid()


    @staticmethod
    def evaluate_group(cells):
        """
        Given a list of cells, find naked pairs
        """
        # for cells that have exactly 2 values, concat the values into a string
        # use that string as a key to a dictionary, using a list of positions (row,col) as the values
        # once all cells have been checked, if any value in the dict has exactly 2 items that means it is a naked pair
        matches = []
        paired_cells = defaultdict(list)

        for cell in cells:
            values = cell.val
            if len(values) != 2:            # ignore every cell that does NOT have 2 possible values (hence pairs)
                continue

            key = str(values)
            paired_cells[key].append(Cell(cell.row, cell.col, values))

        # now that we've checked all cells, see if there's a pair of values in two different cells
        for cell in paired_cells:
            if len(paired_cells[cell]) != 2:              # only look for paired cells
                continue

            for match in paired_cells[cell]:
                matches.append(match)

        return matches

    def execute_group(self, matches, cells):
        """
        Given 2 matching cells whose values contain a naked pair, remove that pair of numbers from possible values
        for all other cells in the group
        Return True if any cells are updated, else false
        """
        if not matches:
            return False

        # the matches var is a list of cells. we want the possible values of those cells (same in both cells)
        # so take the first cell and the 0th and 1th value
        paired_value_0 = matches[0].val[0]      # in unit test below, this would be '4'
        paired_value_1 = matches[0].val[1]      # in unit test below, this would be '6'

        value_removed = False                   # tracks whether or not this routine did anything

        for cell in cells:
            if len(cell.val) == 1:              # ignore cells with values already set
                continue

            # ignore the cells that contain the paired values
            if cell.row == matches[0].row and cell.col == matches[0].col:       # first paired cell
                continue
            if cell.row == matches[1].row and cell.col == matches[1].col:       # second paired cell
                continue

            # otherwise, look for the 2 paired values in all other cells. remove if found
            if paired_value_0 in cell.val:
                self.puzzle.board[cell.row][cell.col].remove(paired_value_0)    # first paired value
                value_removed = True
            if paired_value_1 in cell.val:
                self.puzzle.board[cell.row][cell.col].remove(paired_value_1)    # second paired value
                value_removed = True

        return value_removed

class TestNakePairs(unittest.TestCase):
    def test_evaluate_group(self):
        cells = [
            Cell(0, 0, [4, 6]),         # 4 and 6 are naked pair here
            Cell(0, 1, [7]),
            Cell(0, 2, [4, 6]),         # only other occurrence
            Cell(0, 3, [9]),
            Cell(0, 4, [2]),
            Cell(0, 5, [5]),
            Cell(0, 6, [3, 4, 6]),
            Cell(0, 7, [1]),
            Cell(0, 8, [3, 4, 6, 8])
        ]

        expected = [
            Cell(0, 0, [4, 6]),
            Cell(0, 2, [4, 6])
        ]

        actual = NakedPairs.evaluate_group(cells)
        self.assertEqual(expected, actual)

    def test_evaluate_group_no_pairs(self):
        cells = [
            Cell(0, 0, [4, 6]),         # 4 and 6 are NOT a naked pair here
            Cell(0, 1, [7]),
            Cell(0, 2, [4, 6]),         # 4 and 6 here
            Cell(0, 3, [9]),
            Cell(0, 4, [2]),
            Cell(0, 5, [5]),
            Cell(0, 6, [4, 6]),         # 4 and 6 here too, this makes it NOT a naked pair
            Cell(0, 7, [1]),
            Cell(0, 8, [3, 4, 6, 8])
        ]

        expected = []

        actual = NakedPairs.evaluate_group(cells)
        self.assertEqual(expected, actual)

    def test_full_puzzle(self):
        """
        Integration test using a full puzzle string and validate match found
        """
        from data_collection import SudokuDataCollection
        dc = SudokuDataCollection()
        dc.load_puzzles()
        (ns, hs, np, hp, nt, ht) = dc.run_single_test('76 Hard', level=2)

        self.assertEqual(4, np, 'This puzzle contains 4 known naked pairs at start')

if __name__ == '__main__':
    unittest.main()
