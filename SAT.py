import sys
import math
import numpy as np

class SudokuSolver:

    def __init__(self, input_path, rules):
        self.input_path = input_path
        self.literal_arr = None
        self.unit_clauses = []
        self.rules = rules
        self.clauses = None

        # see comments in ifnameismain part
        with open(input, 'r') as f:
            self.input_list = [line for line in f]
            self.size = math.sqrt(len(input_list[0]) - 1)

        self.nr_literals = self.size ** 3

    def read_input(self) -> None:

        # initialize the literal spoce
        self.literal_arr = np.zeros((self.size, self.size, self.size))

        # TODO: make it work for multiple inputs
        for i, char in enumerate(self.input_list):

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
        '''lmao this whole function isn't even needed fml
            oh wait maybe we do for testing'''

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

    def check_unit_clauses(self):
        for clause in self.clauses:
            if len(clause) == 1:
                
                # TODO: find a more elegant way to do this
                clause_uitgepakt = clause[0]

                # set unit clause literal to true
                self.literal_arr[clause_uitgepakt[0], clause_uitgepakt[1], clause_uitgepakt[2]] == 1


if __name__ == "__main__":

    if len(sys.argv) != 3:
        raise Exception("Unexpected number of arguments, please provide strategy and input file")

    strategy = sys.argv[1]
    input_filename = sys.argv[2]

    with open(input_filename, 'r') as input_file:

        # fetch the correct rules file, we have to make a list of the file in order for this to work
        # note to self: REMEMBER DIFFERENCE BETWEEN FILENAME AND FILE. SHIT AINT A FILE UNTIL YOU'VE OPENED IT
        input_file_list = [input for input in input_file]

        # sneaky detail: input lines end in space, so actual length is always len - 1
        input_line_length = len(input_file_list[0]) - 1

        if input_line_length == 16:
            rules_filename = "rules/sudoku-rules-4x4.txt"
        elif input_line_length == 81:
            rules_filename = "rules/sudoku-rules-9x9.txt"
        elif input_line_length == 256:
            rules_filename = "rules/sudoku-rules-16x16.txt"
        else:
            raise Exception(f"Unexpected sudoku size. Supported sudoku sizes are: 4x4, 9x9, 16x16. Size {math.sqrt(input_line_length)} was found")

    solution_object = SudokuSolver(input_filename, rules_filename)
    solution_object.run()

