
To run all tests:
> python .\main.py

To run data collection (try to solve all input test puzzles in puzzles.txt)
> python .\data_collection.py
Some routines print out results in a format that can be imported into latex report

INFO:
Create an instance:
sudoku = Sudoku(puzzle_str)     # where puzzle str is of the form in puzzles.txt

Print out simple view of a board:
sudoku.print()
Produces something like (blank means cell is unsolved:
8 7|31 |62
523|896|417
 61|27 | 38
-----------
  8|741| 6
 1 |  8| 7
   | 39|18
-----------
 5 | 8 | 9
  4|962|851
 89|5 3| 46
Solved cells: 49 (60%)

For detailed info:
sudoku.print(simple=False)

Prints something like below. Each 3x3 grid represents a single cell and possible values
I.e. the top left cell is 2, neighbor to the right is 4, next right neighbor can be any number (inference rule should remove 2 and 4)
___ ___ 123 ___ 123 123 123 123 123
_8_ _4_ 456 _3_ 456 456 456 456 456
___ ___ 789 ___ 789 789 789 789 789

123 123 123 ___ ___ 123 ___ 123 ___
456 456 456 _5_ _2_ 456 _4_ 456 _7_
789 789 789 ___ ___ 789 ___ 789 ___

123 123 123 123 ___ ___ 123 123 ___
456 456 456 456 _4_ _6_ 456 456 _8_
789 789 789 789 ___ ___ 789 789 ___

___ ___ 123 ___ 123 123 123 ___ ___
_6_ _1_ 456 _7_ 456 456 456 _8_ _4_
___ ___ 789 ___ 789 789 789 ___ ___

123 123 ___ 123 ___ 123 ___ 123 123
456 456 _9_ 456 _6_ 456 _5_ 456 456
789 789 ___ 789 ___ 789 ___ 789 789

___ ___ 123 123 123 ___ 123 ___ ___
_7_ _3_ 456 456 456 _5_ 456 _6_ _1_
___ ___ 789 789 789 ___ 789 ___ ___

___ 123 123 ___ ___ 123 123 123 123
_1_ 456 456 _4_ _7_ 456 456 456 456
___ 789 789 ___ ___ 789 789 789 789

___ 123 ___ 123 ___ ___ 123 123 123
_3_ 456 _2_ 456 _5_ _1_ 456 456 456
___ 789 ___ 789 ___ ___ 789 789 789

123 123 123 123 123 ___ 123 ___ ___
456 456 456 456 456 _2_ 456 _1_ _9_
789 789 789 789 789 ___ 789 ___ ___


