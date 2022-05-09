    #!/usr/bin/python3
import unittest

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
        count = 0
        cell_changed = True  # run init at least once
        while cell_changed:  # keep running when a change is made
            cell_changed = False  # this ensures a change is made every loop

            # TODO search rows
            # TODO search cols
            # TODO search regions

            # TODO once the triples are identified, remove the triple values from all other cells in the group

        return count

    @staticmethod
    def evaluate_group(cells):
        """
        Given a list of cells, find hidden pairs
        """

        # TODO
        raise Exception('not done, Joe or Wadood?')


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

        expected = [
            Cell(0, 1, [5, 6]),
            Cell(0, 4, [6, 9]),
            Cell(0, 7, [5, 9])
        ]

        actual = NakedTriples.evaluate_group(cells)
        self.assertEqual(expected, actual)



if __name__ == '__main__':
    unittest.main()
