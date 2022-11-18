#############################################
# This file deals with most of the I/O action
#############################################

import sys
import math
import numpy as np
from dpll import *
from tqdm import tqdm
import re


# def __init__(self, input_path, rules):
#         self.input_path = input_path
#         self.literal_arr = None
#         self.unit_clauses = []
#         self.rules = rules
#         self.clauses = None

#         # see comments in ifnameismain part
#         with open(input, 'r') as f:
#             self.input_list = [line for line in f]
#             self.size = math.sqrt(len(input_list[0]) - 1)


def read_input(sudoku):
    '''
    input: type=str, sudoku string in format: "..3..4...8. etc")
    output: list of unit clauses

    WORKS
    '''
  
    sudoku_minus_space = sudoku.replace(" ", "")
    unit_clauses = []
    size = math.sqrt(len(sudoku_minus_space))

    # TODO: make it work for multiple inputs
    for i, char in enumerate(sudoku_minus_space):

        if char == ".":
            continue
        else:
            digit = char
            print(digit)

            # + 1 because computer counting starts at 0 but human counting starts at 1
            row = str(int(i // size) + 1)
            column = str(int(i % size) + 1)

            # make a list of the clause so it's corretly represented as a unit clause
            clause = [int(row + column + digit)]
            unit_clauses.append(clause)

    return unit_clauses


def add_rules(unit_clauses, rules_path):
    '''
    input: rule file path (string), list of clauses
    output: list of clauses: unit clauses added to rules. All variables represented as integers

    lmao this whole function isn't even needed fml
    oh wait maybe we do for testing

    WORKS
    '''

    rules = read_DIMACS(rules_path)

    ## PART2: append rules clauses to unit clauses
    clauses = unit_clauses + rules

    return clauses

def read_DIMACS(filename):
    '''
    input: DIMACS file path
    output: list of clauses

    '''

    clauses = []

    with open(filename, 'r') as f:

        lines = f.readlines()

        for line in lines[1:]:

            # add clauses as list of variables to list of clauses. Ignore last element bc this is 0 for each line
            split_clause = line.split(" ")
            split_clause_ints = [int(var) for var in split_clause[:-1]]
            clauses.append(split_clause_ints)

    return clauses

            
def run(input_path, rules_path, heuristic=None):
    '''
    MASTER FUNCTION, currently only works for a single sudoku
    
    input: sudoku file path, rules file path
    output: solved sudoku in dict format
    '''

    satisfiabilities = []
    variables = []

    with open(input_path, 'r') as f:

        lines = f.readlines()

        for line in tqdm(lines):

            unit_clauses = read_input(str(line))
            clauses = add_rules(unit_clauses, rules_path)

            satisfiabilities.append(dpll(clauses, heuristic)[0])
            variables.append(dpll(clauses, heuristic)[1])

        # CODE FOR RUNNING ONE LINE
        # line = lines[0]

        # unit_clauses = read_input(str(line))
        # clauses = add_rules(unit_clauses, rules_path)

        # solutions.append(dpll(clauses))

    return satisfiabilities, variables

def solutions_to_DIMACS(vars_dict, filename):
    '''
    input: dict of variables with values True or False
    output: txt file of solution in DIMACS format

    This output should again be a DIMACS file, but containing only the truth assignment to all variables.
    If your input file is called 'filename', then make sure your outputfile is called 'filename.out'. 
    If there is no solution (inconsistent problem), the output can be an empty file. If there are multiple solutions (eg. non-propert Sudoku) you only need to return a single solution.
    '''

    n_vars = len(vars_dict)
    n_clauses = len(vars_dict)

    # write to file
    with open(f"solutions/{filename}.out", "w") as f:

        # write header
        f.write(f"p cnf {n_clauses} {n_vars}\n")

        # write variables
        for var, value in vars_dict.items():

            if value == True:
                f.write(f"{var} 0\n")
            else:
                f.write(f"{-var} 0\n")
    
    return

if __name__ == "__main__":

    # if len(sys.argv) != 3:
    #     raise Exception("Unexpected number of arguments, please provide strategy and input file")

    # strategy = sys.argv[1]
    # input_filename = sys.argv[2]

    # # get the correct rules file
    # with open(input_filename, 'r') as input_file:

    #     # note to self: REMEMBER DIFFERENCE BETWEEN FILENAME AND FILE. SHIT AINT A FILE UNTIL YOU'VE OPENED IT
    #     # fetch the correct rules file, just make this list so we can count how big the sudoku we're dealing with is
    #     input_file_list = [input for input in input_file]

    #     # sneaky detail: input lines end in space, so actual length is always len - 1
    #     input_line_length = len(input_file_list[0]) - 1

    #     if input_line_length == 16:
    #         rules_filename = "rules/sudoku-rules-4x4.txt"
    #     elif input_line_length == 81:
    #         rules_filename = "rules/sudoku-rules-9x9.txt"
    #     elif input_line_length == 256:
    #         rules_filename = "rules/sudoku-rules-16x16.txt"
    #     else:
    #         raise Exception(f"Unexpected sudoku size. Supported sudoku sizes are: 4x4, 9x9, 16x16. Size {math.sqrt(input_line_length)} was found")

    # # run the program
    # if strategy == '-S1':
    #     print("Solving using strategy 1")
    #     satisfiability, variables = run(input_filename, rules_filename)
    # elif strategy == '-S2':
    #     print("Solving using strategy 2, not implemented yet")
    #     satisfiability, variables = run(input_filename, rules_filename, heuristic='DLCS')
    # elif strategy == '-S3':
    #     print("Solving using strategy 3, not implemented yet")
    #     satisfiability, variables = run(input_filename, rules_filename, heuristic='human')
    # else:
    #     raise Exception("Unexpected strategy, please provide -S1, -S2 or -S3")

    # for i, sat in enumerate(satisfiability):
    #     print(f"Sudoku {i} is satisfiable: {sat}")

    # show_vars = input("Would you like to see the variables that make this sudoku true? (y/n)")

    # if show_vars == "y":
    #     for i, vars in enumerate(variables):
    #         print(f"Variables for sudoku {i}: {vars}")

    # # write solutions to file
    # solutions_to_DIMACS(variables[0], filename="test_output")

    print(read_input("2.1..3..4.7..6.9"))





