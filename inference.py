#!/usr/bin/python3

from abc import ABC, abstractmethod
# import sudoku.Sudoku

# from sudoku import Sudoku


class InferenceRule(ABC):
    """
    Generic parent class for sudoku inference rules

    """
    # from sudoku import Sudoku
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.move_count = 0

    @abstractmethod
    def evaluate(self):
        """
        Find the first cell whose value can be inferred
        If found:
            update inferred cell with value
            remove inferred value from possible values in row, col and subgroup

        NOTE: Make sure to update self.move_count every time a cell is updated
        """
        pass
