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

puzzle_file = 'puzzles.txt'

class SudokuDataCollection(unittest.TestCase):
    def setUp(self):
        self.load_puzzles()

    def load_puzzles(self):
        '''
        Load all puzzles from puzzles.txt into a dictionary
        '''
        new_puzzle = True
        self.puzzles = {}
        with open(puzzle_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                if new_puzzle:
                    name = line
                    new_puzzle = False
                    puzzle_str = ""
                elif line.strip() == '':
                    new_puzzle = True
                    self.puzzles[name] = puzzle_str
                    try:
                        Sudoku(puzzle_str)
                    except:
                        a = 1
                else:
                    puzzle_str += line


    def test_algos(self):
        '''
        Load puzzles.txt
        Run each puzzle through several algo combinations and record performance
        '''
        puzzle_1_easy = self.puzzles['1 Easy']
        sudoku = Sudoku(puzzle_1_easy)

        sudoku.print(simple=False)
        sudoku.print()
        # sudoku.solve()

    def test_all_puzzles(self):
        """
        Print out results for inference rules run against all puzzles
        """
        solved_count = 0
        for puzzle in self.puzzles:
            sudoku = Sudoku(self.puzzles[puzzle])

            start_count = sudoku.get_solved_cell_count()
            sudoku.solve()
            end_count = sudoku.get_solved_cell_count()

            pct = 100 * end_count / 81
            print(f'{puzzle:15s} {start_count:2d} {end_count:2d} {pct:2.0f}%')

            if end_count == 81:
                solved_count += 1

        pct = 100 * solved_count / len(self.puzzles)
        print(f'Solved {solved_count} of {len(self.puzzles)} {pct:2.0f}%')


if __name__ == '__main__':
    unittest.main()
