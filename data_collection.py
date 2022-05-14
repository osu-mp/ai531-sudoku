#!/usr/bin/python3

# AI 531 - Sudoku
# Wadood Alam
# Joe Nguyen
# Matthew Pacey

import time
import unittest
from collections import defaultdict

from naked_singles import NakedSingles
from hidden_singles import HiddenSingles
from simple_BT import solve_simple_BT
from sudoku import Sudoku
from most_constrained import *

puzzle_file = 'puzzles.txt'


class SudokuDataCollection(unittest.TestCase):
# class SudokuDataCollection():

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

    def test_singles_only(self):
        ''''
        Test puzzle with naked single inference only
        '''
        sudoku = Sudoku(self.puzzles['1 Easy'])
        print('start')
        sudoku.print(simple=False)
        # sudoku.init_constraints()
        # print('after constraints initialized')

        print('after constraints initialized')
        ns = NakedSingles(sudoku)
        ns.evaluate()
        sudoku.print(simple=False)
        sudoku.print()
        self.assertTrue(sudoku.is_board_solved())

    def run_single_test(self, puzzle_name, level):
        """
        Run a single puzzle string through solver
        This allows inference tests to access the already loaded puzzles directly
        """
        sudoku = Sudoku(self.puzzles[puzzle_name])
        return sudoku.solve(level=level)

    def test_all_puzzles(self):
        """
        Print out results for inference rules run against all puzzles
        """
        solved_count = 0
        # csv_report = 'puzzle name,given cells,solved cells,solved delta,solved pct,' + \
        #              'naked singles,hidden singles,naked pairs,hidden pairs,hidden triples,naked triples\n'

        for puzzle in self.puzzles:
            sudoku = Sudoku(self.puzzles[puzzle])
            # print(self.puzzles[puzzle])
            # sudoku.print()

            start_count = sudoku.get_solved_cell_count()
            # record the naked singles, hidden singles, pairs, triples from the solve
            # (ns, hs, np, hp, nt, ht) = sudoku.solve(level=4)            # run at max level
            solved_sudoku = solve_most_constrained_var(sudoku)
            # sudoku.print()
            solved_sudoku = solve_simple_BT(sudoku)
            # solved_sudoku.print()
            end_count = solved_sudoku.get_solved_cell_count()

            pct = 100 * end_count / 81
            print(f'{puzzle:15s} {start_count:2d} {end_count:2d} {pct:2.0f}%')
            # csv_report += f'{puzzle},{start_count},{end_count},{end_count-start_count},{pct},{ns},{hs},{np},{hp},{nt},{ht}\n'


            if end_count == 81:
                solved_count += 1

        pct = 100 * solved_count / len(self.puzzles)
        # print(csv_report)
        print(f'Solved {solved_count} of {len(self.puzzles)} {pct:2.0f}%')

    def test_report_data(self):
        """
        Generate data to put into latex report
        """

        print('Fixed Baseline & Backtracking')

        total_puzzles = {}
        total_solved = {}
        avg_time = {}
        avg_ns = {}
        avg_hs = {}
        avg_np = {}
        avg_hp = {}
        avg_nt = {}
        avg_ht = {}
        avg_backtracks = {}

        all_difficulties = ['Easy', 'Medium', 'Hard', 'Evil']

        for difficulty in all_difficulties:
            total_solved[difficulty] = {}
            avg_time[difficulty] = {}

            # print(f'\nDifficulty: {difficulty}')
            for level in range(1, 4):

                puzzle_count = 0
                solved_count = 0
                runtime_sum = 0.
                sum_ns = 0
                sum_hs = 0
                sum_np = 0
                sum_hp = 0
                sum_nt = 0
                sum_ht = 0
                sum_backtracks = 0

                # print(f'Level {level}')

                for puzzle_name in self.puzzles.keys():
                    # each puzzle is named like '10 Hard' so use the name to see if it is the difficulty we're testing
                    if difficulty not in puzzle_name:
                        continue

                    puzzle_count += 1

                    start = time.time()  # get start time
                    # solve puzzle
                    sudoku = Sudoku(self.puzzles[puzzle_name])
                    # (ns, hs, np, hp, nt, ht) = sudoku.solve(level)
                    # (ns, hs, np, hp, nt, ht) = (0, 0, 0, 0, 0, 0)
                    solution = solve_most_constrained_var(sudoku, [])


                    end = time.time()
                    runtime_sum += end - start

                    if level == 3:  # only count singles/pairs/triples at highest level
                        sum_ns += ns
                        sum_hs += hs
                        sum_np += np
                        sum_hp += hp
                        sum_nt += nt
                        sum_ht += ht

                        bt = Sudoku(self.puzzles[puzzle_name])
                        bt.solve_fixed_baseline_backtrack_entry()
                        sum_backtracks += bt.bt_count

                    if sudoku.is_board_solved():
                        solved_count += 1

                total_solved[difficulty][level] = solved_count
                avg_time[difficulty][level] = runtime_sum / puzzle_count
                total_puzzles[difficulty] = puzzle_count

                if level == 3:  # only count singles/pairs/triples at highest level
                    avg_ns[difficulty] = sum_ns  # / puzzle_count
                    avg_hs[difficulty] = sum_hs  # / puzzle_count
                    avg_np[difficulty] = sum_np  # / puzzle_count
                    avg_hp[difficulty] = sum_hp  # / puzzle_count
                    avg_nt[difficulty] = sum_nt  # / puzzle_count
                    avg_ht[difficulty] = sum_ht  # / puzzle_count

                    avg_backtracks[difficulty] = sum_backtracks / puzzle_count

        print('Problems Solved')
        row = ''
        level = 3
        for difficulty in all_difficulties:
            pct = total_solved[difficulty][level] / total_puzzles[difficulty] * 100
            row += ' & %2.0f \\%%' % pct
        print(f'{row} \\\\')

        print('Backtracks')
        row = ''
        for difficulty in all_difficulties:
            row += ' & %d \\' % avg_backtracks[difficulty]
        print(f'{row} \\\\')

        for level in range(1, 4):
            print(f'Level {level}')
            row = ''
            for difficulty in all_difficulties:
                pct = total_solved[difficulty][level] / total_puzzles[difficulty] * 100
                row += ' & %2.0f \\%%' % pct
            print(f'{row} \\\\')

        print('Singles')
        row = ''
        for difficulty in all_difficulties:
            row += ' & %d + %d' % (avg_ns[difficulty], avg_hs[difficulty])
        print(f'{row} \\\\')

        print('Pairs')
        row = ''
        for difficulty in all_difficulties:
            row += ' & %d + %d' % (avg_np[difficulty], avg_hp[difficulty])
        print(f'{row} \\\\')

        print('Triples')
        row = ''
        for difficulty in all_difficulties:
            row += ' & %d + %d' % (avg_nt[difficulty], avg_ht[difficulty])
        print(f'{row} \\\\')

        print('Avg time')
        row = ''
        level = 3  # report average time using all inference rules (level 3)
        for difficulty in all_difficulties:
            row += ' & %1.4f' % avg_time[difficulty][level]
        print(f'{row} \\\\')


    def test_report_data_no_inference(self):
        """
        Generate data to put into latex report
        """

        print('MCV and Fixed Baseline, No Inference')

        total_puzzles = {}
        total_solved = {}
        avg_time = {}
        avg_backtracks = {}

        # TODO: only testing easy, update to all diffs for all data
        all_difficulties = ['Easy', 'Medium', 'Hard', 'Evil']
        # all_difficulties = ['1 Easy']
        for difficulty in all_difficulties:
            total_solved[difficulty] = {}
            avg_time[difficulty] = {}


            puzzle_count = 0
            solved_count = 0
            runtime_sum = 0.
            sum_backtracks = 0


            for puzzle_name in self.puzzles.keys():
                # each puzzle is named like '10 Hard' so use the name to see if it is the difficulty we're testing
                if difficulty not in puzzle_name:
                    continue

                puzzle_count += 1

                start = time.time()  # get start time
                # solve puzzle
                sudoku = Sudoku(self.puzzles[puzzle_name])
                solution = solve_most_constrained_var(sudoku, [], rules=[])

                end = time.time()
                runtime_sum += end - start

                bt = Sudoku(self.puzzles[puzzle_name])
                solved_sudoku, counter = solve_simple_BT(bt)
                sum_backtracks += counter.value

                if sudoku.is_board_solved():
                    solved_count += 1

            total_solved[difficulty] = solved_count
            avg_time[difficulty] = runtime_sum / puzzle_count
            total_puzzles[difficulty] = puzzle_count


            avg_backtracks[difficulty] = sum_backtracks / puzzle_count

        print('Problems Solved')
        row = ''
        level = 3
        for difficulty in all_difficulties:
            pct = total_solved[difficulty] / total_puzzles[difficulty] * 100
            row += ' & %2.0f \\%%' % pct
        print(f'{row} \\\\')

        print('Backtracks')
        row = ''
        for difficulty in all_difficulties:
            row += ' & %d \\' % avg_backtracks[difficulty]
        print(f'{row} \\\\')


        print('Total Solved')
        row = ''
        for difficulty in all_difficulties:
            pct = total_solved[difficulty] / total_puzzles[difficulty] * 100
            row += ' & %2.0f \\%%' % pct
        print(f'{row} \\\\')

        print('Avg time')
        row = ''
        level = 3  # report average time using all inference rules (level 3)
        for difficulty in all_difficulties:
            row += ' & %1.4f' % avg_time[difficulty]
        print(f'{row} \\\\')


if __name__ == '__main__':
    unittest.main()
    # actor = SudokuDataCollection()
    # actor.setUp()
    # actor.test_all_puzzles()
