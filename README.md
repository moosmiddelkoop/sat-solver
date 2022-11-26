SAT solver to solve Sudokus encoded in DIMACS format

To solve a single Sudoku, call SAT.py file, example:

python SAT.py -S1 test_sudokus/sudoku1.cnf

with -S1 being a strategy (S1, S2, or S3)
and test_sudokus/sudoku1.cnf being the sudoku you'd want to solve

a file with the same name as the input but with an added .out extension will be saved in the same place the input file was saved,
and will contain the found variables which will solve the Sudoku, encoded in DIMACS format.

------------------------------------------------------

Most I/O handling happens in SAT.py
Most of the computing functions are in dpll.py
To run an experiment (track multiple sudokus, backtracks, assignments. Save all to an output file and plot backtracks and assignments),
one can run experiment.py
To plot results from experiments one can use plot.py

--------------------------------------------------------

Written by:

Moos Middelkoop, 2788809
@moosmiddelkoop 

Max Feucht, 2742061
@MaxFeucht

Alexia Salomons, 2763078
@AlexiaSalomons