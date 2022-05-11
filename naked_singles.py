#!/usr/bin/python3
import unittest

from cell import Cell
from inference import InferenceRule

class NakedSingles(InferenceRule):
    def evaluate(self):
        """
        http://sudokuessentials.com/sudoku_tips/
        Every Sudoku puzzle will have cells that have only one possible candidate.
        If there aren’t any other candidates showing, Sudoku players call this a naked single.

        Every naked single allows us to safely eliminate that number from all other cells in the
        row, column, and region that the naked single lies in.
        The logic is simple. If there is one cell that contains a single candidate,
        then that candidate is the solution for that cell.
        See link above for example.
        """

        cell_changed = True  # run init at least once
        while cell_changed:  # keep running when a change is made
            cell_changed = False  # this ensures a change is made every loop
            for row in range(9):
                for col in range(9):
                    value = self.puzzle.board[row][col]
                    if len(value) == 1:
                        cell = Cell(row, col, value[0])
                        changed = self.puzzle.solve_cell(cell)
                        if changed:
                            self.move_count += 1
                            cell_changed = True
