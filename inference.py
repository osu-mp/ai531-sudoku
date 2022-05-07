#!/usr/bin/python3

from abc import ABC, abstractmethod


class InferenceRule(ABC):
    """
    Generic parent class for sudoku inference rules

    """
    def __init__(self, puzzle):
        self.puzzle = puzzle

    @abstractmethod
    def evaluate(self):
        """
        Find the first cell whose value can be inferred
        If found:
            update inferred cell with value
            remove inferred value from possible values in row, col and subgroup
        return count of cells changed
        """
        pass
