#!/usr/bin/python3

class Cell:
    """
    Representation of a single cell in the sudoku puzzle
    Includes position (row, col) and list of possible values
    If val is a list of length one, that cell's value is that single number
    Else, the cell can be any of the values in val
    """
    def __init__(self, row, col, val):
        self.row = row
        self.col = col
        self.val = val

    def __eq__(self, other):
        """
        Compare two cells (used for tests)
        """
        return self.row == other.row and self.col == other.col and self.val == other.val

    def __str__(self):
        """
        Print cell
        """
        return(f'Cell: {self.row},{self.col} = {self.val}')
