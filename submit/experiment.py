from SAT import *
from dpll_old import *
import matplotlib.pyplot as plt
import time

def experiment(input_path, heuristic=None, track_time=True):
    '''
    function to keep track of number of backtracks for multiple strategies
    '''

    # get the rules
    rules_path = find_rules(input_path)
    assignments = []
    backtracks = []
    it_per_sec = None
    time_per_it = []
    
    with open(input_path, 'r') as f:
        lines = f.readlines()

        if track_time:
            start = time.time()

        # run over sudokus and save backtracks
        for line in tqdm(lines):

            start = time.time()

            unit_clauses = read_input(str(line))
            clauses = add_rules(unit_clauses, rules_path)
            solution = dpll(clauses, heuristic)
            backtracks.append(solution[1])
            assignments.append(solution[2])

            end = time.time()

            time_per_it.append(end - start)

        if track_time:
            # save time and calculate iterations per second, only for relative comparison! make sure circumstances are the same!
            # this makes it quite a bit slower
            end = time.time()
            diff = end - start
            it_per_sec = len(lines) / diff

    return assignments, backtracks, it_per_sec, time_per_it


    
if __name__ == "__main__":


    # ARGUMENTS: get the input path, strategy and output path
    strategy = sys.argv[1]
    input_path = sys.argv[2]
    output_path = sys.argv[3]

    # create dictionary to map input to correct heuristic
    heuristic_dict = {"-S1": None, "-S2": "DLCS", "-S3": "human"}

    # check if strategy is valid
    if strategy not in heuristic_dict.keys():
        print("Invalid strategy")

    # run the experiment
    assignments, backtracks, speed, time_per_it = experiment(input_path, heuristic_dict[strategy])

    # simple histplot
    y_list = np.linspace(0, len(backtracks), len(backtracks))
    plt.hist(backtracks)
    plt.show()
    plt.hist(assignments)
    plt.show()

    with open(output_path, 'w') as f:
        f.write('BACKTRACKS\n')
        for backtrack in backtracks:
            f.write(f'{str(backtrack)}\n')

        f.write('\nSPEED IN ITERATIONS PER SECOND\n')
        f.write(f'{str(speed)}\n')

        f.write('\nASSIGNMENTS\n')
        for assignment in assignments:
            f.write(f'{str(assignment)}\n')

        f.write('\nTIME PER ITERATION\n')
        for time in time_per_it:
            f.write(f'{str(time)}\n')

 

        