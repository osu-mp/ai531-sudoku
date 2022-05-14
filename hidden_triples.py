# !/usr/bin/python3
import itertools
from typing import List

from cell import Cell
from inference import InferenceRule
import sudoku


def not_appear_other_cells(other_cells: List[Cell], poss_triple_vals: List[int]):
    assert len(poss_triple_vals) == 3
    for cell in other_cells:
        for val in poss_triple_vals:
            if val in cell.val:
                return False
    return True


def appear_triple_cells(triple_cells: List[Cell], poss_triple_vals: List[int]):
    assert len(poss_triple_vals) == 3
    for cell in triple_cells:
        has_at_least_one_val = any(val in cell.val for val in poss_triple_vals)
        if not has_at_least_one_val:
            return False
    return True


def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))


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
        # count = 0
        # cell_changed = True  # run init at least once
        # while cell_changed:  # keep running when a change is made
        #     cell_changed = False  # this ensures a change is made every loop

        # ROW
        for row in range(9):
            cells = self.puzzle.get_row(row)
            self.execute_group(cells)
            self.puzzle.is_board_valid()

        # search cols
        for col in range(9):
            cells = self.puzzle.get_col(col)
            self.execute_group(cells)
            self.puzzle.is_board_valid()

        # search regions
        for reg in range(9):
            cells = self.puzzle.get_region(reg)
            self.execute_group(cells)
            self.puzzle.is_board_valid()

    def execute_triple(self, triple_cells: List[Cell], triple_vals: List[int]):
        for cell in triple_cells:
            new_val = sorted(list(set(cell.val) & set(triple_vals)))
            self.puzzle.board[cell.row][cell.col] = new_val
            cell.val = new_val

    # @staticmethod
    def execute_group(self, cells: List[Cell]):
        """
        Given a list of cells, find hidden pairs
        """
        poss_triple_cell_ids = itertools.combinations(range(len(cells)), 3)

        for triple_cell_ids in poss_triple_cell_ids:
            other_cell_ids = Diff(range(len(cells)), triple_cell_ids)
            triple_cells = [cells[e] for e in triple_cell_ids]
            other_cells = [cells[e] for e in other_cell_ids]

            triple_vals = [cell.val for cell in triple_cells]
            vals = set([val for val in itertools.chain.from_iterable(triple_vals)])
            vals = list(vals)
            if len(vals) < 3:
                continue

            poss_triple_vals = itertools.combinations(vals, 3)
            for triple_vals in poss_triple_vals:
                if not_appear_other_cells(other_cells, triple_vals) \
                        and appear_triple_cells(triple_cells, triple_vals):
                    self.execute_triple(triple_cells, triple_vals)
                    # for cell in triple_cells:
                    #     self.puzzle.board[cell.row][cell.col] = list(set(cell.val) & set(triple_vals))
                    #     cell.val = list(set(cell.val) & set(triple_vals))
        #
        return cells


# class TestHiddenTriples(unittest.TestCase):
#     def test_evaluate_group(self):
#         cells = [
#             Cell(0, 0, [1, 2, 6]),
#             Cell(0, 1, [1, 2, 5, 6]),
#             Cell(0, 2, [4, 5, 8, 9]),  # hidden triple
#             Cell(0, 3, [7]),
#             Cell(0, 4, [1, 4, 6, 8]),  # hidden triple
#             Cell(0, 5, [2, 3, 8, 9]),  # hidden triple
#             Cell(0, 6, [2, 3, 5, 6]),
#             Cell(0, 7, [2, 3, 6]),
#             Cell(0, 8, [2, 3, 5])
#         ]
#
#         expected = [
#             Cell(0, 0, [1, 2, 6]),
#             Cell(0, 1, [1, 2, 5, 6]),
#             Cell(0, 2, [4, 8, 9]),
#             Cell(0, 3, [7]),
#             Cell(0, 4, [4, 8, 9]),
#             Cell(0, 5, [4, 8, 9]),
#             Cell(0, 6, [2, 3, 5, 6]),
#             Cell(0, 7, [2, 3, 6]),
#             Cell(0, 8, [2, 3, 5])
#         ]
#
#         actual = HiddenTriples.execute_group(cells)
#         self.assertEqual(expected, actual)


if __name__ == '__main__':
    # unittest.main()
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
    cells = [
        Cell(0, 0, [1, 2, 6]),
        Cell(0, 1, [1, 2, 5, 6]),
        Cell(0, 2, [4, 5, 8, 9]),  # hidden triple
        Cell(0, 3, [7]),
        Cell(0, 4, [1, 4, 6, 8]),  # hidden triple
        Cell(0, 5, [2, 3, 8, 9]),  # hidden triple
        Cell(0, 6, [2, 3, 5, 6]),
        Cell(0, 7, [2, 3, 6]),
        Cell(0, 8, [2, 3, 5])
    ]

    expected = [
        Cell(0, 0, [1, 2, 6]),
        Cell(0, 1, [1, 2, 5, 6]),
        Cell(0, 2, [4, 8, 9]),
        Cell(0, 3, [7]),
        Cell(0, 4, [4, 8]),
        Cell(0, 5, [8, 9]),
        Cell(0, 6, [2, 3, 5, 6]),
        Cell(0, 7, [2, 3, 6]),
        Cell(0, 8, [2, 3, 5])
    ]
    expected_vals = [cell.val for cell in expected]

    test_sudoku = sudoku.Sudoku(EVIL_SUDOKU)
    test_sudoku.board[0][0] = [1, 2, 6]
    test_sudoku.board[0][1] = [1, 2, 5, 6]
    test_sudoku.board[0][2] = [4, 5, 8, 9]  # hidden triple
    test_sudoku.board[0][3] = [7]
    test_sudoku.board[0][4] = [1, 4, 6, 8]  # hidden triple
    test_sudoku.board[0][5] = [2, 3, 8, 9]  # hidden triple
    test_sudoku.board[0][6] = [2, 3, 5, 6]
    test_sudoku.board[0][7] = [2, 3, 6]
    test_sudoku.board[0][8] = [2, 3, 5]
    # for i in range(1, 9):
    #     for j in range(0, 9):
    #         test_sudoku.board[i][j] = []

    actor = HiddenTriples(puzzle=test_sudoku)
    actor.execute_group(cells)
    print(actor.puzzle.board[0])
    # assert (actor.puzzle.board[0] == expected_vals)
