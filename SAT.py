import sys
import math

def sudoku_to_dimacs(sudoku):

    clauses = []
    nr_clauses = 0
    nr_literals = math.sqrt(len(sudoku))

    for i, char in enumerate(sudoku):
        if char == ".":
            continue
        else:
            digit = char
            row = i // 4
            column = i % 4
            clauses.append(f"{digit}{row}{column}")
            nr_clauses += 1

    print(f"p cnf {nr_clauses} {nr_literals}")
    for clause in clauses:
        print(clause + " 0")

    return

if __name__ == "__main__":

    if len(sys.argv) != 3:
        raise Exception("Unexpected number of arguments, please provide strategy and input file")

    strategy = sys.argv[1]
    input_file = sys.argv[2]

    sudoku_to_dimacs(input_file)

