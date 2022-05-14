#!/usr/bin/python3

# AI 531 - Sudoku
# Wadood Alam
# Joe Nguyen
# Matthew Pacey

import unittest

from cell import Cell
from hidden_singles import HiddenSingles
from naked_singles import NakedSingles
from sudoku import Sudoku

puzzle_1_easy = '''240 300 000  
                000 520 407
                000 046 008
                610 700 084
                009 060 500 
                730 005 061 
                100 470 000 
                302 051 000 
                000 002 019'''

puzzle_2_medium = '''020 004 000
003 000 204
140 080 503
030 802 000
200 000 006
000 409 050
402 070 081
807 000 600
000 600 070

'''

puzzle_3_hard = '''170 000 006
006 090 040
300 070 000
000 900 030
094 020 870
030 005 000
000 060 001
080 010 500
500 000 082'''

class TestSudoku(unittest.TestCase):
    """
    Unit tests and data collection for Sudoku routines
    """
    def test_loadPuzzlePrintSimple(self):
        """
        Test initializing a puzzle with a puzzle string
        Validate print function works
        """
        board = Sudoku(puzzle_1_easy)
        expected = '''24 |3  |   
   |52 |4 7
   | 46|  8
-----------
61 |7  | 84
  9| 6 |5  
73 |  5| 61
-----------
1  |47 |   
3 2| 51|   
   |  2| 19
Solved cells: 33 (41%)
'''
        result = board.print()

        self.assertEqual(result, expected)

    def test_loadPuzzlePrintComplex(self):
        """
        Test initializing a puzzle with a puzzle string
        Validate print complex function works
        """
        board = Sudoku(puzzle_1_easy)

        expected = '''___ ___ 123 ___ 123 123 123 123 123 
_2_ _4_ 456 _3_ 456 456 456 456 456 
___ ___ 789 ___ 789 789 789 789 789 
                                                                                                            
123 123 123 ___ ___ 123 ___ 123 ___ 
456 456 456 _5_ _2_ 456 _4_ 456 _7_ 
789 789 789 ___ ___ 789 ___ 789 ___ 
                                                                                                            
123 123 123 123 ___ ___ 123 123 ___ 
456 456 456 456 _4_ _6_ 456 456 _8_ 
789 789 789 789 ___ ___ 789 789 ___ 
                                                                                                            
___ ___ 123 ___ 123 123 123 ___ ___ 
_6_ _1_ 456 _7_ 456 456 456 _8_ _4_ 
___ ___ 789 ___ 789 789 789 ___ ___ 
                                                                                                            
123 123 ___ 123 ___ 123 ___ 123 123 
456 456 _9_ 456 _6_ 456 _5_ 456 456 
789 789 ___ 789 ___ 789 ___ 789 789 
                                                                                                            
___ ___ 123 123 123 ___ 123 ___ ___ 
_7_ _3_ 456 456 456 _5_ 456 _6_ _1_ 
___ ___ 789 789 789 ___ 789 ___ ___ 
                                                                                                            
___ 123 123 ___ ___ 123 123 123 123 
_1_ 456 456 _4_ _7_ 456 456 456 456 
___ 789 789 ___ ___ 789 789 789 789 
                                                                                                            
___ 123 ___ 123 ___ ___ 123 123 123 
_3_ 456 _2_ 456 _5_ _1_ 456 456 456 
___ 789 ___ 789 ___ ___ 789 789 789 
                                                                                                            
123 123 123 123 123 ___ 123 ___ ___ 
456 456 456 456 456 _2_ 456 _1_ _9_ 
789 789 789 789 789 ___ 789 ___ ___ 
                                                                                                            
Solved cells: 33 (41%)
'''
        result = board.print(simple=False)
        self.assertEqual(result, expected)

    def test_remove_poss_value(self):
        """
        Functional test for remove_poss_value
        validate possible values removed from row, col and subgroup
        """
        sudoku = Sudoku(puzzle_1_easy)

        # expected possible values at row 0, col 2 before routine (all values since it is blank)
        self.assertEqual(sudoku.board[0][2], [1, 2, 3, 4, 5, 6, 7, 8, 9])
        # expected possible values at row 1, col 0 before (all values since it is blank)
        self.assertEqual(sudoku.board[1][0], [1, 2, 3, 4, 5, 6, 7, 8, 9])

        # ROW TEST: verify 4 removed from possible values for row 0
        row = 0
        # run remove_poss for value of 4 at 0,1, verify 4 removed from column 1
        cell = Cell(row, 1, 4)
        sudoku.solve_cell(cell)
        # 4 should now be missing from possible values in column 1
        self.assertEqual(sudoku.board[row][2], [1, 2, 3, 5, 6, 7, 8, 9])

        # COL TEST: verify 5 removed from possible values for column 3
        col = 3
        # run remove_poss for value of 7 at row 3, col 3 (second subgroup of row 1)
        cell = Cell(3, col, 7)
        sudoku.solve_cell(cell)
        # verify 7 removed from possible values for row 5, col 4 (same subgroup)
        self.assertEqual(sudoku.board[5][col], [1, 2, 3, 4, 5, 6, 8, 9])

        # SUBGROUP: remove 9 from bottom right subroup
        # run remove_poss_values for value of 9 at 8,8, verify 9 removed from col 7 in row 6
        cell = Cell(8, 8, 9)
        sudoku.solve_cell(cell)
        # 2 should now be missing from possible values
        self.assertEqual(sudoku.board[6][7], [1, 2, 3, 4, 5, 6, 7, 8])

    def test_naked_singles(self):
        """
        Test naked singles on easy puzzle
        """
        sudoku = Sudoku(puzzle_1_easy)
        (ns, hs, np, hp, nt, ht) = sudoku.solve(level=1)
        self.assertEqual(ns, 66, "There are 66 naked singles in easy 1 puzzle")

    def test_hidden_singles(self):
        """
        Test hidden singles on easy puzzle
        """
        sudoku = Sudoku(puzzle_3_hard)
        (ns, hs, np, hp, nt, ht) = sudoku.solve(level=1)
        self.assertEqual(hs, 12, "There are 12 hidden singles in the 3 Hard puzzle")

    def test_get_bt_puzzle(self):
        """
        Unit test for get_bt_puzzle
        Convert the puzzle 3d array into a 2d array for the backtracking algo
        """
        puzzle_str = '''
        002 090 600
        609 000 000
        480 006 000
        008 402 090
        300 000 007
        070 309 100
        000 600 051
        000 000 204
        007 080 300
        '''
        sudoku = Sudoku(puzzle_str)

        expected = [
            [0, 0, 2, 0, 9, 0, 6, 0, 0],
            [6, 0, 9, 0, 0, 0, 0, 0, 0],
            [4, 8, 0, 0, 0, 6, 0, 0, 0],
            [0, 0, 8, 4, 0, 2, 0, 9, 0],
            [3, 0, 0, 0, 0, 0, 0, 0, 7],
            [0, 7, 0, 3, 0, 9, 1, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 5, 1],
            [0, 0, 0, 0, 0, 0, 2, 0, 4],
            [0, 0, 7, 0, 8, 0, 3, 0, 0]
        ]
        actual = sudoku.get_bt_puzzle()
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()

    from data_collection import SudokuDataCollection
    SudokuDataCollection().test_all_puzzles()
