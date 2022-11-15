#############################################
# This file deals with most of the I/O action
#############################################

import sys
import math
import numpy as np
from dpll import *
from tqdm import tqdm


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
  
    sudoku_minus_space = sudoku[:-1]
    unit_clauses = []
    size = math.sqrt(len(sudoku_minus_space))

    # TODO: make it work for multiple inputs
    for i, char in enumerate(sudoku_minus_space):

        if char == ".":
            continue
        else:
            digit = char

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

    ## PART1: turn rules file into list of clauses
    rules_cnf = []

    # turn rules txt file into list of clauses. Loop over all but the first line
    with open(rules_path, 'r') as f:

        lines = f.readlines()

        for clause in lines[1:]:

            # add clauses as list of variables to list of clauses. Ignore last element bc this is 0 for each line
            split_clause = clause.split(" ")
            split_clause_ints = [int(var) for var in split_clause[:-1]]
            rules_cnf.append(split_clause_ints)

    ## PART2: append rules clauses to unit clauses
    clauses = unit_clauses + rules_cnf

    return clauses

            
def run(input_path, rules_path):
    '''
    MASTER FUNCTION, currently only works for a single sudoku
    
    input: sudoku file path, rules file path
    output: solved sudoku in dict format
    '''

    solutions = []

    with open(input_path, 'r') as f:

        lines = f.readlines()

        for line in tqdm(lines):

            unit_clauses = read_input(str(line))
            clauses = add_rules(unit_clauses, rules_path)

            solutions.append(dpll(clauses))

    return solutions

def solutions_to_cnf():
    # TODO: this
    pass

if __name__ == "__main__":

    if len(sys.argv) != 3:
        raise Exception("Unexpected number of arguments, please provide strategy and input file")

    strategy = sys.argv[1]
    input_filename = sys.argv[2]

    with open(input_filename, 'r') as input_file:

        # note to self: REMEMBER DIFFERENCE BETWEEN FILENAME AND FILE. SHIT AINT A FILE UNTIL YOU'VE OPENED IT
        # fetch the correct rules file, just make this list so we can count how big the sudoku we're dealing with is
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

    print(run(input_filename, rules_filename))





