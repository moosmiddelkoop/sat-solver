
def check_solution(solution_path):

    true_count = 0

    with open(solution_path, 'r') as f:

        lines = f.readlines()

        # loop over all but the first line of solution cnf
        for line in lines[1:]:
            
            # if literal value is true, add 1 to true_count
            if line[0] != "-":
                true_count += 1
        
        return true_count

if __name__ == "__main__":

    trues = check_solution('solutions/test_output.out')
    print(trues)