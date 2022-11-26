from SAT import *
import matplotlib.pyplot as plt
import numpy as np
import time

# argument handling
heuristic = sys.argv[1]
clauses = read_DIMACS(sys.argv[2])
output_path = sys.argv[3]

start = time.time()

solution = dpll(clauses, heuristic)
print(solution)

end = time.time()

satisfiability = (solution[0][0])
variables = (solution[0][1])
backtracks = (solution[1])
assignments = (solution[2])
depths = (solution[3])
speed = (end - start)

print(f"Satisfiability: {satisfiability}")

see_backtracks = input("Do you want to see the number of backtracks? (y/n): ")
if see_backtracks == 'y':
    print(backtracks)

see_assignments = input("Do you want to see the number of assignments? (y/n): ")
if see_assignments == 'y':
    print(assignments)

see_vars = input("Do you want to see the variables? (y/n): ")
if see_vars == 'y':
    print(variables)

x_axis = np.linspace(0, len(depths), len(depths))
y_axis = depths

with open(output_path, 'w') as f:
    f.write('BACKTRACKS\n')
    f.write(f'{str(backtracks)}\n')

    f.write('\nSPEED IN SECONDS\n')
    f.write(f'{str(speed)}\n')

    f.write('\nASSIGNMENTS\n')
    f.write(f'{str(assignments)}\n')

    f.write('\nDEPTHS\n')
    for depth in depths:
        f.write(f'{str(depth)}\n')


# quickly plot depths
            
plt.title(f'Plot of the depth of the search tree over time. heuristic = {heuristic}')
plt.plot(x_axis, y_axis)
plt.show()
plt.savefig(f'figs/depths/sudoku5_depths.png')
