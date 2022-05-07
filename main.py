#!/usr/bin/python3

# AI 531 - Sudoku
# Wadood Alam
# Joe Nguyen
# Matthew Pacey

import csv
import time
import unittest

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
        sudoku.remove_poss_value(4, row, 1)
        # 4 should now be missing from possible values in column 1
        self.assertEqual(sudoku.board[row][2], [1, 2, 3, 5, 6, 7, 8, 9])

        # COL TEST: verify 5 removed from possible values for column 3
        col = 3
        # run remove_poss for value of 7 at row 3, col 3 (second subgroup of row 1)
        sudoku.remove_poss_value(7, 3, col)
        # verify 7 removed from possible values for row 5, col 4 (same subgroup)
        self.assertEqual(sudoku.board[5][col], [1, 2, 3, 4, 5, 6, 8, 9])

        # SUBGROUP: remove 9 from bottom right subroup
        # run remove_poss_values for value of 9 at 8,8, verify 9 removed from col 7 in row 6
        sudoku.remove_poss_value(9, 8, 8)
        # 2 should now be missing from possible values
        self.assertEqual(sudoku.board[6][7], [1, 2, 3, 4, 5, 6, 7, 8])

    def test_naked_singles(self):
        """
        Test naked singles on easy puzzle
        """
        sudoku = Sudoku(puzzle_1_easy)
        print('Before naked singles:')
        sudoku.print()
        ns = NakedSingles(sudoku)
        count = ns.evaluate()
        print('After naked singles:')
        sudoku.print()
        self.assertEqual(count, 384, "There are 384 naked single moves in easy 1 puzzle")

    def skip_test_solve_easy(self):
        '''
        Test solving easy puzzle
        '''
        # TODO
        sudoku = Sudoku(puzzle_1_easy)

        sudoku.print(simple=False)
        sudoku.print()
        # sudoku.solve()

if __name__ == '__main__':
    unittest.main()
