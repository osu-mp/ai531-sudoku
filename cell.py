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
