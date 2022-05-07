#!/usr/bin/python3

# AI 531 - Sudoku
# Wadood Alam
# Joe Nguyen
# Matthew Pacey

from naked_singles import NakedSingles


"""
Assignment Description
------------------------------------------

In this assignment you will be implementing a solver for SuDoKu.

SuDoKu is a constraint satisfaction problem, with all-diff constraints on each row, column, and box. The variables are cells and the values are numbers 1-9. You are going to implement backtracking search with constraint propagation. It maintains all possible candidate values, i.e., the current domain, for each cell after each assignment. The baseline system implements forward checking which removes candidate values for a variable when it violate some constraints, given the currently assigned values for other variables.

The search begins by storing all possible values for each of the empty spots. Then it does constraint propagation through domain-specific inference rules. When the constraint propagation converges, then: 
- if no candidates left for some cell, then backtrack from the current state. 
- else pick a cell, and assign it a consistent value (keep other choices of values as options to backtrack to; there is no need to backtrack over the cell choice since all cells need to be filled).

Experiment with two different ways of picking a cell.

Fixed  Baseline. Use a fixed order, say, row-wise and top to bottom.
Most Constrained Variable: Pick a slot that has the least number of values in its domain.
Apply the following inference rules in the given priority order, i.e., keep applying rule 1 as long as it applies. When it does not, apply rule 2, and go back to rule 1 if it applies. In general, apply rule k only when rules 1...k-1 are not applicable. The inference terminates when no rule is applicable, at which point a search action (assignment) is taken. At any search state, the program maintains the set of assignments made in that state, and the candidate numbers available in all other cells. Here are the inference rules to be tried in that sequence.  

Naked Singles
Hidden Singles.
Naked Pairs.
Hidden Pairs.
Naked Triples.
Hidden Triples.
Please refer to this page (Links to an external site.)Links to an external site. for an explanation of these rules. Conduct experiments with the following subsets of rules.

No inference
Naked and Hidden Singles.
Naked and Hidden Singles and Pairs
Naked and Hidden Singles, Pairs, and Triples.
Give a reasonable fixed bound on the number of search steps, say 1000, for each experiment.

There is a set of sample problems here (Links to an external site.)Links to an external site.. The numbers are written in the file row-wise, with 0 representing empty slots. Each team should try to solve all the problems, starting with the easy ones. Report the number of problems solved and the number of backtracks with each problem. Experts appear to grade the problems by the complexity of rules needed to solve them without backtracking. Is this conjecture roughly correct? Grade each problem, by the set of rules used in solving it. Report also the average number of filled-in numbers (in the beginning) for each of these types of problems. Would this accurately reflect the difficulty of the problem?

Report your results in the form of a mini-paper as you did for the other two assignments. Give the pseudocode for the algorithm. Discuss how the results vary with the difficulty of the problems, and the effectiveness of the most-constrained variable heuristic compared to fixed selection. Also report on the effectiveness of rule subsets in reducing the search. Is the number of backtracks reduced by increased inference rules? What about the total time for solving the puzzles? Please feel free to include any other observations.
"""



class Sudoku:
    totalNodes = 0  # global counter of total nodes in total tree

    def __init__(self, puzzle_str):
        """
        Init the Sudoku board with a puzzle string
        The board is a 3d array: board[row][col][values] where:
            row and col represent the 2D board (i.e. row=0, col=3 is the fourth cell in the first row)
            values is a list of possible numbers for the given cell at row,col
            If a cell starts off as blank (0 in puzzle_str input) that means values 1-9 are valid
            The inference rules will reduce this list as they execute
            If values has only one number, that is the final value
        """
        self.board = []
        self.build_board_from_str(puzzle_str)

    def build_board_from_str(self, puzzle_str):
        """
        Given a string like below, convert it to the data structure used by the solvers

        Example puzzle (0 = blank, 1-9 given value for each cell)
        240 300 000
        000 520 407
        000 046 008
        610 700 084
        009 060 500
        730 005 061
        100 470 000
        302 051 000
        000 002 019
        """
        # get rid of spaces and newlines
        puzzle_str = puzzle_str.replace(' ', '')
        puzzle_str = puzzle_str.replace('\n', '')

        # validate input
        if len(puzzle_str) != 81:
            raise Exception('Invalid puzzle, expected 81 numbers (0 for blank)')

        # init board (9x9 grid where each cell is a list of acceptable values 1-9)
        self.board = [[[0 for cell in range(9)] for col in range(9)] for row in range(9)]
        row = 0
        col = 0
        for cell in puzzle_str.strip():
            cell = int(cell)
            if cell == 0:
                self.board[row][col] = list(range(1, 10))
            else:
                self.board[row][col] = [cell]

            col += 1
            if col == 9:            # at the final column, move to the next row
                col = 0
                row += 1

    def is_board_solved(self):
        raise Exception('TODO')

    def is_board_filled(self):
        """
        Return True if the all cells have a single value, else False
        :return:
        """
        for row in range(9):
            for col in range(9):
                if len(self.board[row][col]) > 1:
                    return False

        return True

    def is_board_valid(self):
        """
        Return True if all cells are consistent, otherwise False
        Only cells with a single value are checked (cells with multiple values are not final values)
        To be consistent each row, col and 3x3 grid can only have 1-9 (no repeats)
        """
        raise Exception('not implemented')

    def print(self, simple=True, screen=True):
        """
        Print the current board
        If simple is True, this prints a 9x9 grid of single values (blanks for unsolved cells)
        If simple is False, this prints a 9x9 grid of 3x3 grids where each smaller grid
        represents the possible values (blank value for invalid values)
        :return:
        """
        solved = 0  # count number of solved cells

        if simple:
            board = ""
            for row in range(9):
                for col in range(9):
                    cell = self.board[row][col]
                    if len(cell) == 1:
                        board += str(cell[0])
                        solved += 1
                    else:
                        board += ' '
                    if col in [2, 5]:           # put divider between each 3 cols
                        board += '|'
                board += '\n'                   # newline after each row
                if row in [2, 5]:               # print divider between each 3 rows
                    board += '-' * 11 + '\n'
        else:
            # for complex prints, print a 3x3 grid for each cell in the larger 9x9 grid
            # the smaller 3x3 grid will contain all acceptable values for that cell
            # if the cell is set, the final value will be in the center of the grid

            # the big board is 9 cells by 3 rows/cols in each cell -> 27x27 grid
            bigBoard = [['_' for col in range(27)] for row in range(27)]
            for row in range(9):
                for col in range(9):
                    cell = self.board[row][col]
                    if len(cell) == 1:
                        bigBoard[row * 3 + 1][col * 3 + 1] = str(cell[0])       # put values in center
                        solved += 1
                    else:
                        for i in range(1, 10):
                            # each cell looks like:
                            # 123
                            # 456
                            # 789
                            # where the cell shares multiple rows with 9 other cells
                            # so we need to use the values 1-9 to find where those values go
                            if i in cell:
                                # only include values that apply for that cell
                                # i.e. if 456 are disallowed because of other cells
                                # the second row will be blank
                                subRow = row * 3 + (i - 1) // 3
                                subCol = col * 3 + (i - 1) % 3
                                bigBoard[subRow][subCol] = str(i)

            # create the string that will be used for the final printout
            # use spacers between each cell
            board = ""
            rowCount = 0
            colCount = 0
            for row in bigBoard:
                for col in row:
                    board += col
                    colCount += 1
                    if colCount == 3:       # new cell marker, add spacer
                        colCount = 0
                        board += ' '
                board += '\n'
                rowCount += 1
                if rowCount == 3:
                    board += ' ' * (81+27) + '\n'       # 81 numbers plus 27 spacers
                    rowCount = 0
        board += 'Solved cells: %d (%2.f%%)\n' % (solved, solved * 100 / 81)
        print(board)
        return board                            # for unit tests

    def __str__(self):
        """
        Print the current board (for debug)
        """
        return self.print()

    def init_inference(self):
        """
        Run the initial inference after the puzzle has been initialized
        For every cell that has a single value, eliminate that single value for
        every other cell in that row, col and subgroup
        """
        raise Exception('deprecated')

    def remove_poss_value(self, val, row, col):
        """
        Given a single value at row, col ensure that that value is not listed
        as a possible value in any row, column or subgroup
        Return count of possible values removed (0 means no actions)
        """
        count = 0
        # check row first by checking all cols in target row
        for c in range(9):
            if c == col:            # ignore the cell with the single value
                continue
            if val in self.board[row][c]:
                self.board[row][c].remove(val)
                # print('Removed ROW possible value of %d at %d,%d' % (val, row, c))
                count += 1

        # check col next by checking all rows in target col
        for r in range(9):
            if r == row:            # ignore the cell with the single value
                continue
            if val in self.board[r][col]:
                self.board[r][col].remove(val)
                # print('Removed COL possible value of %d at %d,%d' % (val, row, c))
                count += 1

        # find the subgroup for this cell and check all neighbors
        row_start = (row // 3) * 3      # start of the subgroup row and col
        col_start = (col // 3) * 3      # round down to previous 3 group
        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if r == row and c == col:       # ignore cell with single value
                    continue
                # if the target value is a possible value, remove it
                if val in self.board[r][c]:
                    self.board[r][c].remove(val)
                    count += 1

        return count
        
    def solve(self):
        ns = NakedSingles(self)

        move_cnt = 0
        while ns.evaluate():
            move_cnt += 1