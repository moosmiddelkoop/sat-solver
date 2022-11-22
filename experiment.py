from SAT import *
from dpll import *
import matplotlib.pyplot as plt

def experiment(input_path, heuristic=None):
    '''
    function to keep track of number of backtracks for multiple strategies
    '''

    # get the rules
    rules_path = find_rules(input_path)
        
    backtracks = []
    with open(input_path, 'r') as f:
        lines = f.readlines()

        # run over sudokus and save backtracks
        for line in tqdm(lines):
            unit_clauses = read_input(str(line))
            clauses = add_rules(unit_clauses, rules_path)
            solution = dpll(clauses, heuristic)
            backtracks.append(solution[2])

    return backtracks

if __name__ == "__main__":

    OUTPUT_PATH = "backtracks-damnhard-S3.txt"

    # get the input path and strategy
    input_path = sys.argv[2]
    strategy = sys.argv[1]

    if strategy == "-S1":
        heuristic = None
    elif strategy == "-S2":
        heuristic = "DLCS"
    elif strategy == "-S3":
        heuristic = "human"
    else:
        print("Invalid strategy")
        exit()

    # run the experiment
    backtracks = experiment(input_path, heuristic)

    y_list = np.linspace(0, len(backtracks), len(backtracks))
    plt.hist(backtracks)
    plt.show()

    with open(OUTPUT_PATH, 'w') as f:
        for backtrack in backtracks:
            f.write(str(backtrack))

    # vvv autogenerated but nice list lets look into this haha vvv    
        # elif strategy == 'random':
            
        # elif strategy == 'MOM':
            
        # elif strategy == 'JW':
            
        # elif strategy == 'DLIS':
            
        # elif strategy == 'DLCS':
            
        # elif strategy == 'VSIDS':
            
        # elif strategy == 'VSIDS+':
            
        # elif strategy == 'VSIDS++':
            
        # else:
        #     print("Invalid strategy. Please choose from: DCLS, human, random, MOM, JW, DLIS, DLCS, VSIDS, VSIDS+, VSIDS++")
        #     return None


        