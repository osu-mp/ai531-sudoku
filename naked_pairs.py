    #!/usr/bin/python3
import unittest

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
        count = 0
        cell_changed = True  # run init at least once
        while cell_changed:  # keep running when a change is made
            cell_changed = False  # this ensures a change is made every loop

            # TODO search rows
            # TODO search cols
            # TODO search regions

            # TODO once the pairs are identified, remove the paired values from all other cells in the group
            # i.e. for unit test below, 4 and 6 would be removed from all but cell 0,0 and cell 0,2

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
            Cell(0, 0, [4, 6]),         # 4 and 6 are naked pair here
            Cell(0, 1, [7]),
            Cell(0, 2, [4, 6]),         # only other occurence
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



if __name__ == '__main__':
    unittest.main()
