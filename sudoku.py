#!/usr/bin/python3

# AI 531 - Sudoku
# Wadood Alam
# Joe Nguyen
# Matthew Pacey

from unicodedata import digit
from cell import Cell
from naked_singles import NakedSingles
from hidden_singles import HiddenSingles
from naked_pairs import NakedPairs
from hidden_pairs import HiddenPairs
from naked_triples import NakedTriples
from hidden_triples import HiddenTriples
import math

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
        # get rid of spaces and newlines, tabs
        puzzle_str = puzzle_str.replace(' ', '')
        puzzle_str = puzzle_str.replace('\n', '')
        puzzle_str = puzzle_str.replace('\t', '')

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
        """
        The board is solved when all cells are filled and all cells are valid
        (1-9 in each row, col and region, no repeats)
        """
        return self.is_board_filled() and self.is_board_valid()

    def get_solved_cell_count(self):
        """
        Return the number of solved cells (only have 1 possible value)
        :return:
        """
        count = 0
        for row in range(9):
            for col in range(9):
                if len(self.board[row][col]) == 1:
                    count += 1

        return count

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
        # check all rows
        for row in range(9):
            cells = self.get_row(row)
            if not self.is_cell_group_valid(cells):
                self.print()
                raise Exception(f'Row invalid: {row}')

        # check all cols
        for col in range(9):
            cells = self.get_row(row)
            if not self.is_cell_group_valid(cells):
                raise Exception(f'Col invalid: {col}')

        # check all regions
        for reg in range(9):
            cells = self.get_region(reg)
            if not self.is_cell_group_valid(cells):
                raise Exception(f'Region invalid: {reg}')

        return True

    def is_cell_group_valid(self, cells):
        """
        Given a group of 9 cells (row, col or region), return True if the current config is valid, else False
        The config is valid if cells that only have 1 number do not have any repeats in other numbers
        """
        values = []
        for cell in cells:
            values.append(cell.val)
        return self.is_group_valid(values)

    def print(self, simple=True, screen=True):
        """
        Print the current board
        If simple is True, this prints a 9x9 grid of single values (blanks for unsolved cells)
        If simple is False, this prints a 9x9 grid of 3x3 grids where each smaller grid
        represents the possible values (blank value for invalid values)
        :return:
        """
        solved = 0  # count number of solved cells
        board = ""

        if simple:
            
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

    def get_row(self, row, omit_col=None):
        """
        Get all cells in the given row
        Optional: if an index is given for omit_col that column's cell will not be included
            This is used when the caller wants to do something to everything except the given cell
        """
        cells = []
        for col in range(9):
            if omit_col is not None and omit_col == col:
                continue
            cell = Cell(row, col, self.board[row][col])
            cells.append(cell)

        return cells

    def get_col(self, col, omit_row=None):
        """
        Get all cells in the given column
        Optional: if an index is given for omit_row that row's cell will not be included
            This is used when the caller wants to do something to everything except the given cell
        """
        cells = []
        for row in range(9):
            if omit_row is not None and omit_row == row:
                continue
            cell = Cell(row, col, self.board[row][col])
            cells.append(cell)

        return cells

    def get_group(self, row, col, omit_cell=False):
        """
        Given a cell, return addresses/vals of all cells in that 3x3 group
        If omit_cell is True, the given cell will not be included in the list
        Default behavior is to include the given cll
        """
        cells = []

        row_start = (row // 3) * 3  # start of the subgroup row and col
        col_start = (col // 3) * 3  # round down to previous 3 group
        for r in range(row_start, row_start + 3):
            for c in range(col_start, col_start + 3):
                if omit_cell and r == row and c == col:       # ignore the given cell
                    continue
                cell = Cell(r, c, self.board[r][c])
                cells.append(cell)

        return cells

    def get_region(self, region_num):
        """
        Return the cells in the given region number
        The regions are numbered 0 through 8, 0 is the upper left, 8 is the lower right
        """
        if region_num == 0:                     # top left
            return self.get_group(0, 0)
        elif region_num == 1:
            return self.get_group(0, 3)         # top mid
        elif region_num == 2:
            return self.get_group(0, 6)         # top right
        elif region_num == 3:
            return self.get_group(3, 0)         # left mid
        elif region_num == 4:
            return self.get_group(3, 3)         # center
        elif region_num == 5:
            return self.get_group(3, 6)         # right mid
        elif region_num == 6:
            return self.get_group(6, 0)         # bottom left
        elif region_num == 7:
            return self.get_group(6, 3)         # bottom mid
        elif region_num == 8:
            return self.get_group(6, 6)         # bottom right
        raise Exception('Invalid region: %d' % region_num)

    def solve_cell(self, cell: Cell):
        """
        Given a cell  (at row,col) set the value for that cell and remove that value from
        all neighbors in the same row, col and 3x3 region

        Return count of possible values removed (0 means no actions)

        This should be called whenever a number is assigned (remove that number as possible from related cells)
        """
        count = 0
        row = cell.row
        col = cell.col
        val = cell.val

        # check row first by checking all cols in target row
        for neighbor in self.get_row(row, omit_col=col):
            if val in neighbor.val:
                self.board[row][neighbor.col].remove(val)
                # print('Removed ROW possible value of %d at %d,%d' % (val, row, c))
                count += 1

                # TODO : if the updated cell only has one value, update its neighbors
                # if len(self.board[row][neighbor.col]) == 1:
                #     count += self.solve_cell(Cell(row, neighbor.col, self.board[row][neighbor.col][0]))

                # TODO : mpacey added this to debug that board is always in a good state
                # it will decrease performance, so it should be removed once the
                # algo has been verified more
                self.is_board_valid()

        # check col next by checking all rows in target col
        for neighbor in self.get_col(col, omit_row=row):
            if val in neighbor.val:
                self.board[neighbor.row][col].remove(val)
                # print('Removed COL possible value of %d at %d,%d' % (val, row, c))
                count += 1

                # TODO : if the updated cell only has one value, update its neighbors
                # if len(self.board[neighbor.row][col]) == 1:
                #     count += self.solve_cell(Cell(row, neighbor.col, self.board[neighbor.row][col][0]))

                # TODO : mpacey added this to debug that board is always in a good state
                # it will decrease performance, so it should be removed once the
                # algo has been verified more
                self.is_board_valid()

        # find the subgroup for this cell and check all neighbors
        for neighbor in self.get_group(row, col, omit_cell=True):
            if val in self.board[neighbor.row][neighbor.col]:
                self.board[neighbor.row][neighbor.col].remove(val)
                count += 1

                # TODO : if the updated cell only has one value, update its neighbors
                # if len(self.board[neighbor.row][neighbor.col]) == 1:
                #     count += self.solve_cell(Cell(neighbor.row, neighbor.col, self.board[neighbor.row][neighbor.col][0]))

                # TODO : mpacey added this to debug that board is always in a good state
                # it will decrease performance, so it should be removed once the
                # algo has been verified more
                self.is_board_valid()

        return count

    def init_constraints(self):
        """
        After the board has been initialized, iterate through all solved cells
        and update the constraints of related cells.
        For example, if the cell at 0,1 is 4 that means that 4 can be removed from the domain
        for all cells in row 0, all cells in column 1, and all cells in the first 3x3 region
        """
        for row in range(9):
            for col in range(9):
                value = self.board[row][col]
                if len(value) == 1:                  # if number given
                    self.solve_cell(Cell(row, col, value[0]))

    def is_row_valid(self, row):
        """
        Return True if the single values for each cell in the row are valid, else False
        Valid means numbers 1 through 9 with no repeats
        """
        values = []
        for col in range(9):
            values.append(self.board[row][col])

        return self.is_group_valid(values)

    def is_col_valid(self, col):
        """
        Return True if the single values for each cell in the col are valid, else False
        Valid means numbers 1 through 9 with no repeats
        """
        values = []
        for row in range(9):
            values.append(self.board[row][col])

        return self.is_group_valid(values)

    def is_subgroup_valid(self, row, col):
        """
        Return True if the single values for each cell in the 3x3 subgroup are valid, else False
        Valid means numbers 1 through 9 with no repeats
        """
        values = []
        for cell in self.get_group(row, col):
            values.append(cell.val)

        return self.is_group_valid(values)

    def is_group_valid(self, values):
        """
        Return True if the given values are valid (1-9 with no repeats)
        Ignore values with multiple values as those cells are not set yet
        Input can be row, col or subroup values
        """
        used = []
        for value in values:
            if len(value) == 0:         # group must have 1 or more values
                return False
            elif len(value) > 1:          # ignore cells that do not have single values
                continue
            if value[0] in used:        # selected value already exists in input, return False
                return False
            used.append(value[0])       # otherwise add to used list

        return True
   
    # Prints board for backtracking
    def printBoard(self, board):
        for i in range(0, 9):
            for j in range(0, 9):
                print(board[i][j], end=" ")
            print()
    # Checks if the digit is valid in desired position
    def is_valid(self, digit, board, row, col):
        """
        Checks 3 is value is possible or not with 3 conditions:
        1. Check repetation in column
        2. Check repetation in row
        3. Check repetation in 3x3 grid

        """
        # Checks for repeated values in column
        for col_counter in range(0,9):
            if board[row][col_counter] == digit:
                return False

        # Checks for repeated values in row
        for row_counter in range(0,9):
            if board[row_counter][col] == digit:
                return False

        # Checks for repeated values in 3x3 grid
        row_for_small_grid = math.floor(row / 3) * 3
        col_for_small_grid = math.floor(col / 3) * 3
        for miniRow in range(0,3):
            for miniCol in range(0,3):
                if board[row_for_small_grid + miniRow][col_for_small_grid + miniCol] == digit:
                    return False

        return True

    def get_bt_puzzle(self):
        """
        Return the current puzzle in the form that solve_fixed_baseline_backtrack expects
        BT expects a 2D array like this:
        [
            [0, 0, 2, 0, 9, 0, 6, 0, 0],
            [6, 0, 9, 0, 0, 0, 0, 0, 0],
            [4, 8, 0, 0, 0, 6, 0, 0, 0],
            [0, 0, 8, 4, 0, 2, 0, 9, 0],
            [3, 0, 0, 0, 0, 0, 0, 0, 7],
            [0, 7, 0, 3, 0, 9, 1, 0, 0],
            [0, 0, 0, 6, 0, 0, 0, 5, 1],
            [0, 0, 0, 0, 0, 0, 2, 0, 4],
            [0, 0, 7, 0, 8, 0, 3, 0, 0]
        ]
        So convert the self.board 3D list into a 2D list and put a 0 in cells that do not have a single value
        """
        bt_puzzle = []
        for row in range(9):
            this_row = []
            for col in range(9):
                cell_value = self.board[row][col]
                if len(cell_value) == 1:
                    this_row.append(cell_value[0])
                else:
                    this_row.append(0)
            bt_puzzle.append(this_row
                             )
        return bt_puzzle

    def solve_fixed_baseline_backtrack(self, bt_count):
    # Format for taking in a board(unsolved) board in the following format: [[row1],[row2],...,[row9]]
    # TODO: Conversion from str board to a list of arrays may cause an issue? not sure. The correct format for the algo is: e.g puzzle(line 505)
    # NOTE: test_BT.py created to individually test the fixed_baseline BT algo.
        puzzle = [
        [0, 0, 2, 0, 9, 0, 6, 0, 0],
        [6, 0, 9, 0, 0, 0, 0, 0, 0],
        [4, 8, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 8, 4, 0, 2, 0, 9, 0],
        [3, 0, 0, 0, 0, 0, 0, 0, 7],
        [0, 7, 0, 3, 0, 9, 1, 0, 0],
        [0, 0, 0, 6, 0, 0, 0, 5, 1],
        [0, 0, 0, 0, 0, 0, 2, 0, 4],
        [0, 0, 7, 0, 8, 0, 3, 0, 0]
        ]
        puzzle_2_medium = '''020 004 000
    003 000 204
    140 080 503
    030 802 000
    200 000 006
    000 409 050
    402 070 081
    807 000 600
    000 600 070
    '''
        # puzzle =  self.build_board_from_str(puzzle_2_medium)
        for row in range(0, 9):
            for col in range(0, 9):
                if puzzle[row][col] == 0:
                    for digit in range(1, 10):
                        if self.is_valid(digit, puzzle, row, col):
                            puzzle[row][col] = digit
                            self.solve_fixed_baseline_backtrack()
                            bt_count = bt_count + 1
                            puzzle[row][col] = 0
                    return   
        print(bt_count)            
        self.printBoard(puzzle)


    def solve_most_constrained_var(self):
        """

        """
        # TODO get most constrained variable
        raise Exception('TODO Joe')

    def solve(self, level=0):
        """
        Try to solve this puzzle using inference rules
        All inference rules are disabled by default
        The 'level' param inputs translate to:
            0 = no inference (default)
            1 = singles only
            2 = singles and pairs only
            3 = singles, pairs, and triples
        """

        ns = NakedSingles(self)
        hs = HiddenSingles(self)
        np = NakedPairs(self)
        hp = HiddenPairs(self)
        nt = NakedTriples(self)
        ht = HiddenTriples(self)

        while True:
            solved_count = self.get_solved_cell_count()

            if level >= 1:
                # naked singles first
                ns.evaluate()

                # next try hidden singles
                hs.evaluate()

            if level >= 2:
                # next try pairs
                np.evaluate()
                hp.evaluate()

            if level >= 3:
                # next try triples
                nt.evaluate()
                ht.evaluate()

            # if no new cells were solved, exit
            if solved_count == self.get_solved_cell_count():
                break

        return (ns.move_count, hs.move_count, np.move_count, hp.move_count, nt.move_count, ht.move_count)



