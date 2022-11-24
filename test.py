from SAT import *

clauses = read_DIMACS(sys.argv[1])
HEURISTIC = None

solution = dpll(clauses, HEURISTIC)

satisfiability = (solution[0])
variables = (solution[1])
backtracks = (solution[2])

print(f"Satisfiability: {satisfiability}")

see_backtracks = input("Do you want to see the number of backtracks? (y/n): ")

if see_backtracks == 'y':
    print(backtracks)

see_vars = input("Do you want to see the variables? (y/n): ")

if see_vars == 'y':
    print(variables)

