############################
# Important! Literals are unsigned, variables are signed
# Literals and variables are represented as integers
# Therefore clauses are lists of integers
############################

from copy import deepcopy

test_clauses = [[1, 2, 3], [1, -2], [1, -3], [-2, 3]]
literals = [1, 2, 3]

def get_vars(clauses):
    '''
    input: 2D array of clauses
    output: dictionary of literals with values none
    '''

    vars = dict()
    for clause in clauses:
        for var in clause:

            # absolute of the var so the value assigned to it can represent the sign
            vars[abs(var)] = None

    return vars

found_literals = []


def simplify_clauses(clauses, variable):
    """
    input: clauses list and variable (signed literal) based on which to simplify

    returns: simplified clauses list
    """
    
    clauses_copy = deepcopy(clauses)

    for i, clause in enumerate(clauses):
        
        # For True literals: remove whole clause from knowledge base
        if variable in clause:
            clauses_copy.remove(clause)

    for clause in clauses_copy:
        
        # For False literals: remove literal from clause
        if -variable in clause:
            clause.remove(-variable)
                
    return clauses_copy



def check_result(clauses):
    """
    XXXX
    """
    
    # SAT: No filled clauses anymore
    if len(clauses) == 0:
        return True

    # contradiction/UNSAT if any empty clause is included in the knowledge base
    for clause in clauses:
        if len(clause) == 0:
            return False

    # if len([clause for clause in clauses if len(clause) == 0]) >= 1:
    #     return False
    
    else:
        return None


def solve(clauses, var_dict):
    """
    Recursive DPLL solver
    """

    # Create deepcopies of clauses and literals up to this point
    temp_clauses = deepcopy(clauses)
    temp_vars = deepcopy(var_dict)

    # handle unit clauses
    temp_clauses, temp_vars = handle_unit(temp_clauses, temp_vars)

    satisfiable = check_result(temp_clauses)
    if satisfiable != None: 
        return satisfiable, temp_vars
    
    # Extract key of first literal that == None
    next_literal = [k for (k, v) in temp_vars.items() if v == None][0]

    # First: for literal = FALSE
    temp_vars[next_literal] = False # Truth Assignment
    variable = -next_literal
    temp_clauses = simplify_clauses(temp_clauses, variable)
    result = solve(temp_clauses, temp_vars)
    if(result[0]): 
        return result

    #Then: try literal = True
    temp_vars[next_literal] = True
    variable = next_literal
    temp_clauses = simplify_clauses(temp_clauses, variable)
    return solve(temp_clauses, temp_vars)


        
def handle_unit(clauses, var_dict):
    '''
    input: clauses list and variable dictionary
    returns: updated clauses list and updated variable dictionary

    sets all unit literals to true in the variable dict
    removes pure literals from the clauses list

    A bit of a weird construction because simplifying the clauses causes new clauses to be unit clauses, therefore
    You'd need to start over every time you handle a unit clause
    '''

    i = 0
    while i < len(clauses):

        if len(clauses[i]) == 1:

            # unpack variable from unit clause
            variable = clauses[i][0]
            clauses = simplify_clauses(clauses, variable)

            # set literal to true
            if variable > 0:
                var_dict[variable] = True

            # in this case the literal is the unsigned version of the var and needs to be set to false
            elif variable < 0:
                var_dict[-variable] = False
            else:
                raise Exception("zero is not allowed as a variable")
                
            i = 0

        else:
            i += 1

    return clauses, var_dict
    
    
def dpll(clauses):
    '''
    MASTER FUNCTION
    '''
    # get variable dict
    variables = get_vars(clauses)   

    # check if problem is already solved 
    # TODO: fix this
    satisfiable = check_result(clauses)
    if satisfiable != None: 
        return satisfiable, variables

    # solve it
    return solve(clauses, variables)


def jeroslaw_heuristic(clauses, vars_dict):

    '''Jeroslow-Wang Two Sided Heuristic'''

    count_dict = {}
    pos_count, neg_count = 0,0
    for l in vars_dict.keys():
        for clause in clauses:
            if l in clause: pos_count += (2 ** -len(clause))
            if -l in clause: neg_count += (2 ** -len(clause))
        total_count = pos_count + neg_count
        count_dict.update({l: [total_count, pos_count, neg_count]})

    max_count = max([value[0] for value in count_dict.values()])
    max_key = [key for key, value in count_dict.items() if value[0] == max_count][0]
    
    #Assignment:
    assignment = True if count_dict[max_key][1] > count_dict[max_key][2] else False
    
    return (max_key, assignment)

if __name__ == "__main__":

    test_clauses = [[1, 2, 3], [1, -2], [1, -3], [-2, 3]]
    literals = [1, 2, 3]


    # Small test cases provided below

    # TRUE               
    # clauses  = [[1, -5, 4, 2], [-1, 5, 3, 4, 2], [-3, -4, 2], [3], [5]]

    # FALSE
    # clauses  = [[3, 1, 2], [3, 1, -2], [3, -1, 2], [-3, 1, 2], 
        # [3, -1, -2], [-3, 1, -2], [-3, -1, 2], [-3, -1, -2]]
                    
    # TRUE
    # clauses  = [[3, 1, -2], [-3, -1, 2], [-3, 1, -2]]

    # FALSE
    clauses = [[-4, 5], [-5, 4], [-4, -5], [4, 5], [1, 3, 2], [3, -2, -1]]

    print(dpll(clauses))
