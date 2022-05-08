#!/usr/bin/python3
import unittest

from inference import InferenceRule

class NakedSingles(InferenceRule):
    def evaluate(self):
        """
        http://sudokuessentials.com/sudoku_tips/
        Every Sudoku puzzle will have cells that have only one possible candidate.
        If there aren’t any other candidates showing, Sudoku players call this a naked single.

        Every naked single allows us to safely eliminate that number from all other cells in the
        row, column, and region that the naked single lies in.
        The logic is simple. If there is one cell that contains a single candidate,
        then that candidate is the solution for that cell.
        See link above for example.
        """
        count = 0
        cell_changed = True  # run init at least once
        while cell_changed:  # keep running when a change is made
            cell_changed = False  # this ensures a change is made every loop
            for row in range(9):
                for col in range(9):
                    cell = self.puzzle.board[row][col]
                    if len(cell) == 1:
                        changed = self.puzzle.remove_poss_value(cell[0], row, col)
                        if changed:
                            count += changed
                            cell_changed = True

        return count

    def evaluate_group(self, values):
        """
        Given a list of cells with multiple values, find a match
        """

class TestNakeSingles(unittest.TestCase):
    def test_evaluate_group(self):
        values = [
            [2, 6, 7],      # naked 7
            [2, 6],
            [2, 6],
            [2, 5, 6],
            [4, 5]          # nake 4
        ]
        pass

if __name__ == '__main__':
    unittest.main()
