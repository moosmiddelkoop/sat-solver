
test_clauses = [[1, 2, 3], [1, -2], [1, -3], [-2, 3]]
literals = [1, 2, 3]

def get_vars(clauses):
    '''
    input: 2D array of clauses
    output: dictionary of variables with values none

    WORKS
    '''

    vars = dict()
    for clause in clauses:
        for var in clause:
            vars[var] = None

    return vars

found_literals = []


def simplify_clauses(clauses, literal):
    """
    XXXX
    """
    
    for clause in clauses:

        if literal in clause:
                clauses.remove(clause)
            
        elif -literal in clause:
                clause.remove(literal)
                
    return clauses

def check_result(clauses):
    """
    XXXX
    """
    
    # SAT: No v
    if len(clauses) == 0:
        found_literals.append(literal)
        return True

    # contradiction/UNSAT
    elif len([clause for clause in clauses if len(clause) == 0]) >= 1:
        found_literals.remove(literal)
        return False


def solver2(clauses, literal):

    global found_literals
    temp_clauses = clauses.deepcopy()

    # First: for literal == FALSE
    # PUT TRUTH ASSIGNMENT (FALSE) HERE
    temp_clauses = simplify_clauses(temp_clauses, literal)


    # SAT
    if len(temp_clauses) == 0:
        found_literals.append(literal)
        return True

    # contradiction/UNSAT
    elif len([clause for clause in temp_clauses if len(clause) == 0]) >= 1:
        found_literals.remove(literal)
        return False
    
    new_literal = literal + 1

    found_literals.append(new_literal)

    # NEXT STEP (how do we keep track of literals when taking next steps (maybe dictionary works))
    if solver2(temp_clauses, new_literal) == True:
        return True

    else:
        return solver2(temp_clauses, -new_literal)


# solver2()

# get_vars test
print(get_vars(test_clauses))