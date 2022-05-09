    #!/usr/bin/python3
import unittest

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
        count = 0
        cell_changed = True  # run init at least once
        while cell_changed:  # keep running when a change is made
            cell_changed = False  # this ensures a change is made every loop

            # TODO search rows
            # TODO search cols
            # TODO search regions

            # TODO once the pairs are identified, remove the paired values from all other cells in the group
            # i.e. for unit test below, 2 and 9 would be removed from all but cell 0,0 and cell 0,2

        return count

    @staticmethod
    def evaluate_group(cells):
        """
        Given a list of cells, find hidden pairs
        """

        # TODO
        raise Exception('not done, Joe or Wadood?')


class TestNakePairs(unittest.TestCase):
    def test_evaluate_group(self):
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

        actual = HiddenPairs.evaluate_group(cells)
        self.assertEqual(expected, actual)



if __name__ == '__main__':
    unittest.main()
