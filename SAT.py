##############################################################################
# This file deals with most of the I/O action                                #
# Only accepts one sudoku at a time in cnf format as per the assignment      #
##############################################################################

import sys
import math
import numpy as np
from dpll import *
from tqdm import tqdm
import re


def read_input(sudoku):
    '''
    input: type=str, sudoku string in format: "..3..4...8. etc")
    output: list of unit clauses

    WORKS
    '''
  
    sudoku_minus_space = sudoku[:-1] if sudoku[-1] == "\n" else sudoku
    unit_clauses = []
    size = math.sqrt(len(sudoku_minus_space))

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

            
def run(clauses, heuristic):
    '''
    MASTER FUNCTION, currently only works for a single sudoku
    
    input: sudoku clauses, heuristic
    output: 
    - satisfiability (boolean)
    - variables: (dict of variables with values True or False)
    - backtracks: (number of backtracks performed)
    - decisions: (number of decisions made, basically a count of non-forced moves)
    '''

    solution = dpll(clauses, heuristic)

    satisfiability = (solution[0][0])
    variables = (solution[0][1])
    backtracks = (solution[1])
    decisions = (solution[2])

    return satisfiability, variables, backtracks, decisions

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
    with open(filename, "w") as f:

        # write header
        f.write(f"p cnf {n_clauses} {n_vars}\n")

        # write variables
        for var, value in vars_dict.items():

            if value == True:
                f.write(f"{var} 0\n")
            else:
                f.write(f"{-var} 0\n")
    
    return


def find_rules(input_path):
    '''
    input: sudoku filepath
    output: rule filepath to use
    '''

    with open(input_path, 'r') as input_file:

        input_file_list = [input for input in input_file]

        # sneaky detail: input lines end in space, so actual length is always len - 1
        input_line_length = len(input_file_list[0]) - 1

        if input_line_length == 16:
            rules_path = "rules/sudoku-rules-4x4.txt"
        elif input_line_length == 81:
            rules_path = "rules/sudoku-rules-9x9.txt"
        else:
            raise Exception(f"Unexpected sudoku size. Supported sudoku sizes are: 4x4 and 9x9. Size {math.sqrt(input_line_length)} was found")

    return rules_path


if __name__ == "__main__":
    
    if len(sys.argv) != 3:
        raise Exception("Unexpected number of arguments, please provide strategy and input file")

    strategy = sys.argv[1]
    input_path = sys.argv[2]
    output_path = input_path + ".out"
    print(output_path)

    clauses = read_DIMACS(input_path)
 
    # run the program
    if strategy == '-S1':
        print("Solving using DPLL without heuristics")
        satisfiability, variables, backtracks, assignments = run(clauses, heuristic=None)
    elif strategy == '-S2':
        print("Solving using the DLCS heuristic")
        satisfiability, variables, backtracks, assignments = run(clauses, heuristic='DLCS')
    elif strategy == '-S3':
        print("Solving using the Human heuristic")
        satisfiability, variables, backtracks, assignments = run(clauses, heuristic='human')
    else:
        raise Exception("Unexpected strategy, please provide -S1, -S2 or -S3")
    
    # write solutions to file
    solutions_to_DIMACS(variables, filename=output_path)

    print(f"The sudoku: {input_path} is satisfiable: {satisfiability}.")

    see_backtracks = input("Do you want to see the number of backtracks? (y/n): ")
    if see_backtracks == 'y':
        print(backtracks)

    see_assignments = input("Do you want to see the number of decisions made? (y/n): ")
    if see_assignments == 'y':
        print(assignments)

    show_vars = input("Would you like to see the variables that make this sudoku true? (y/n): ")
    if show_vars == "y":
        print(variables)




