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

class SudokuDataCollection(unittest.TestCase):
    def load_puzzles(self):
        '''
        Load all puzzles from puzzles.txt into a dictionary
        '''
        # TODO
        raise Exception('TODO')

    def test_algos(self):
        '''
        Load puzzles.txt
        Run each puzzle through several algo combinations and record performance
        '''
        # TODO
        sudoku = Sudoku(puzzle_1_easy)

        sudoku.print(simple=False)
        sudoku.print()
        # sudoku.solve()


if __name__ == '__main__':
    unittest.main()
