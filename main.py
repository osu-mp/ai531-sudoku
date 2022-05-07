#!/usr/bin/python3

# AI 531 - Sudoku
# Wadood Alam
# Joe Nguyen
# Matthew Pacey

import csv
import time
import unittest

from sudoku import Sudoku

class TestSudoku(unittest.TestCase):
    """
    Unit tests and data collection for Sudoku routines
    """
    def test_loadPuzzlePrintSimple(self):
        """
        Test initializing a puzzle with a puzzle string
        Validate print function works
        """
        puzzleStr = '''240 300 000 
000 520 407
000 046 008
610 700 084
009 060 500 
730 005 061 
100 470 000 
302 051 000 
000 002 019'''

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
'''
        board = Sudoku(puzzleStr)
        result = board.print()

        self.assertEqual(result, expected)

    def test_loadPuzzlePrintComplex(self):
        """
        Test initializing a puzzle with a puzzle string
        Validate print complex function works
        """
        puzzleStr = '''240 300 000 
000 520 407
000 046 008
610 700 084
009 060 500 
730 005 061 
100 470 000 
302 051 000 
000 002 019'''

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
                                                                                                            
'''
        board = Sudoku(puzzleStr)
        result = board.print(simple=False)
        self.assertEqual(result, expected)

    def test_solve_easy(self):
        '''
        Test solving easy puzzle
        '''
        puzzleStr = '''240 300 000 
        000 520 407
        000 046 008
        610 700 084
        009 060 500 
        730 005 061 
        100 470 000 
        302 051 000 
        000 002 019'''

        sudoku = Sudoku(puzzleStr)
        sudoku.solve()

if __name__ == '__main__':
    unittest.main()
