import sys
import math
import numpy as np

class SudokuSolver:

    def __init__(self, input, rules):
        self.input = input
        self.literal_arr = None
        self.size = math.sqrt(len(self.input[0]))
        self.nr_literals = self.size ** 3
        self.unit_clauses = []
        self.rules = rules
        self.clauses = None


    def read_input(self) -> None:

        # initialize the literal spoce
        self.literal_arr = np.zeros((self.size, self.size, self.size))

        for i, char in enumerate(self.input):

            if char == ".":
                continue
            else:
                digit = char
                row = i // self.size
                column = i % self.size
                self.unit_clauses.append(f"{digit}{row}{column}")

            # set unit clauses to true
            self.literal_arr[row, column, digit] == 1


    def add_rules(self) -> None:

        ## PART1: turn rules file into list of clauses
        rules_cnf = []

        # turn rules txt file into list of clauses. Loop over all but the first line
        with open(self.rules, 'r') as f:
            for clause in f[1:]:

                # add clauses as list of variables to list of clauses. Ignore last element bc this is 0 for each line
                split_clause = clause.split[" "]
                rules_cnf.append(split_clause[:-1])

        ## PART2: append rules clauses to unit clauses
        self.clauses = self.unit_clauses + rules_cnf


    def DPLL(self):
        '''Uses literal 3d array and clauses list'''
        pass

                
    def run(self) -> None:
        self.read_input()
        self.add_rules()


if __name__ == "__main__":

    if len(sys.argv) != 3:
        raise Exception("Unexpected number of arguments, please provide strategy and input file")

    strategy = sys.argv[1]
    input_file = sys.argv[2]

    # fetch the correct rules file
    if len(input_file[0]) == 16:
        rules_file = "rules/sudoku-rules-4x4.txt"
    elif len(input_file[0]) == 81:
        rules_file = "rules/sudoku-rules-9x9.txt"
    elif len(input_file[0]) == 256:
        rules_file = "rules/sudoku-rules-16x16.txt"
    else:
        raise Exception("Unexpected sudoku size. Supported sudoku sizes are: 4x4, 9x9, 16x16")

    solution_object = SudokuSolver(input_file, rules_file)
    solution_object.run()

