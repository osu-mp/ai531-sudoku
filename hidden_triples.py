    #!/usr/bin/python3
import unittest

from cell import Cell
from inference import InferenceRule

class HiddenTriples(InferenceRule):
    def evaluate(self):
        """
        http://sudokuessentials.com/sudoku_tips/
        Hidden triples are much harder to spot. They will occur in harder puzzles.
        Hidden triples like naked triples are restricted to three cells in a row, column, or region.
        Hidden triples like hidden pairs have additional digits that camouflage the three candidates.

        If you look at the example at the left, you will see three cells circled in red.
        These are the hidden triples. Can you spot them?

        You are right, they are 4, 8, and 9. Remove the extra numbers from the cells circled in red
        Do you think hidden triples are tough to find? Try quads.
        """
        count = 0
        cell_changed = True  # run init at least once
        while cell_changed:  # keep running when a change is made
            cell_changed = False  # this ensures a change is made every loop

            # TODO search rows
            # TODO search cols
            # TODO search regions

            # TODO once the triples are identified, triples the paired values from all other cells in the group
            # i.e. for unit test below, 4, 8, and 9 would be removed from all but cell 0,2 and cell 0,4 and 0,5

        return count

    @staticmethod
    def evaluate_group(cells):
        """
        Given a list of cells, find hidden pairs
        """

        # TODO
        raise Exception('not done, Joe or Wadood?')


class TestHiddenTriples(unittest.TestCase):
    def test_evaluate_group(self):
        cells = [
            Cell(0, 0, [1, 2, 6]),
            Cell(0, 1, [1, 2, 5, 6]),
            Cell(0, 2, [4, 5, 8, 9]),           # hidden triple
            Cell(0, 3, [7]),
            Cell(0, 4, [1, 4, 6, 8]),           # hidden triple
            Cell(0, 5, [2, 3, 8, 9]),           # hidden triple
            Cell(0, 6, [2, 3, 5, 6]),
            Cell(0, 7, [2, 3, 6]),
            Cell(0, 8, [2, 3, 5])
        ]

        expected = [
            Cell(0, 2, [4, 8, 9]),
            Cell(0, 4, [4, 8, 9]),
            Cell(0, 5, [4, 8, 9])
        ]

        actual = HiddenTriples.evaluate_group(cells)
        self.assertEqual(expected, actual)



if __name__ == '__main__':
    unittest.main()
