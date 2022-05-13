#!/usr/bin/python3

import unittest

from cell import Cell
from inference import InferenceRule

class HiddenSingles(InferenceRule):
    def evaluate(self):
        """
        http://sudokuessentials.com/sudoku_tips/
        In the example at the left there are two hidden singles.
        Hidden singles have only one place they can go.
        The extra candidates in the cell “hide” the single solution.

        In this example, the third cell from the top is a seven.
        Likewise in the bottom cell the only number that can go there is a four
        See link above for example.
        """

        cell_changed = True  # run init at least once
        while cell_changed:  # keep running when a change is made
            cell_changed = False  # this ensures a change is made every loop

            # check rows
            for row in range(9):
                cells = self.puzzle.get_row(row)
                matches = self.evaluate_group(cells)
                # print(f'Current puzzle, checking row {row}')
                # self.puzzle.print(simple=False)
                for match in matches:
                    # print(f'Operating on match: {match}')
                    self.puzzle.board[match.row][match.col] = [match.val]
                    changed = self.puzzle.solve_cell(match)
                    self.move_count += 1
                    cell_changed = True
                    self.puzzle.is_board_valid()

            # # check cols
            for col in range(9):
                cells = self.puzzle.get_col(col)
                matches = self.evaluate_group(cells)
                for match in matches:
                    self.puzzle.board[match.row][match.col] = [match.val]
                    changed = self.puzzle.solve_cell(match)
                    self.move_count += 1
                    cell_changed = True
                    self.puzzle.is_board_valid()

            # # check regions
            for n in range(9):
                cells = self.puzzle.get_region(n)
                matches = self.evaluate_group(cells)
                for match in matches:
                    self.puzzle.board[match.row][match.col] = [match.val]
                    changed = self.puzzle.solve_cell(match)
                    self.move_count += 1
                    cell_changed = True
                    self.puzzle.is_board_valid()

    def evaluate2d(self):
        cell_changed = True  # run init at least once
        while cell_changed:  # keep running when a change is made
            cell_changed = False  # this ensures a change is made every loop

            # check rows
            for row in range(9):
                cells = self.puzzle.get_row(row)
                matches = self.evaluate_group(cells)
                # print(f'Current puzzle, checking row {row}')
                # self.puzzle.print(simple=False)
                for match in matches:
                    # print(f'Operating on match: {match}')
                    self.puzzle.board[match.row][match.col] = [match.val]
                    changed = self.puzzle.solve_fixed_baseline_backtrack_entry(0)
                    self.move_count += 1
                    cell_changed = True
                    self.puzzle.is_board_valid()

            # # check cols
            for col in range(9):
                cells = self.puzzle.get_col(col)
                matches = self.evaluate_group(cells)
                for match in matches:
                    self.puzzle.board[match.row][match.col] = [match.val]
                    changed = self.puzzle.solve_fixed_baseline_backtrack_entry(0)
                    self.move_count += 1
                    cell_changed = True
                    self.puzzle.is_board_valid()

            # # check regions
            for n in range(9):
                cells = self.puzzle.get_region(n)
                matches = self.evaluate_group(cells)
                for match in matches:
                    self.puzzle.board[match.row][match.col] = [match.val]
                    changed = self.puzzle.solve_fixed_baseline_backtrack_entry(0)
                    self.move_count += 1
                    cell_changed = True
                    self.puzzle.is_board_valid()

    @staticmethod
    def evaluate_group(cells):
        """
        Given a list of cells with multiple values, find a match
        """
        # list each cell where a value is possible,
        # if only one cell, that is a hidden single
        # key = number (1-9), value = list of cells where it could be
        poss_cells = {}
        set_vals = []                   # values that are already set (ignore these as hidden singles)
        for cell in cells:
            # ignore cells with values set
            if len(cell.val) == 1:
                set_vals.append(cell.val[0])
            else:
                for val in cell.val:
                    if val in poss_cells:
                        poss_cells[val].append((cell.row, cell.col))
                    else:
                        poss_cells[val] = [(cell.row, cell.col)]

        # if any values in poss_cells have a single value, that is a hidden single
        hidden_singles = []
        for value in poss_cells:
            if value in set_vals:                       # if a value has already been set in a cell, ignore
                continue
            if len(poss_cells[value]) == 1:
                row, col = poss_cells[value][0]
                hidden_singles.append(Cell(row, col, value))

        return hidden_singles


class TestHiddenSingles(unittest.TestCase):
    def test_evaluate_group(self):
        cells = [
            Cell(0, 0, [1]),
            Cell(0, 1, [8]),
            Cell(0, 2, [2, 6, 7]),      # hidden 7 (only in group)
            Cell(0, 3, [2, 6]),
            Cell(0, 4, [3]),
            Cell(0, 5, [2, 6]),
            Cell(0, 6, [2, 5, 6]),
            Cell(0, 7, [9]),
            Cell(0, 8, [4, 5])          # hidden 4 (only in group)
        ]

        expected_hidden = [
            Cell(0, 2, 7),
            Cell(0, 8, 4)
        ]

        actual_hidden = HiddenSingles.evaluate_group(cells)
        self.assertEqual(expected_hidden, actual_hidden)

    def test_evaluate_group_10_medium(self):
        """
        This was a failing case before set_vals was introduced (produced a match where there was none)
        """
        cells = [
            Cell(0, 0, [1, 2, 7]),
            Cell(0, 1, [8]),
            Cell(0, 2, [9]),
            Cell(0, 3, [1, 5]),
            Cell(0, 4, [5]),
            Cell(0, 5, [3]),
            Cell(0, 6, [2, 7]),
            Cell(0, 7, [4]),
            Cell(0, 8, [4])
        ]

        expected_hidden = []

        actual_hidden = HiddenSingles.evaluate_group(cells)
        self.assertEqual(expected_hidden, actual_hidden)



if __name__ == '__main__':
    unittest.main()
