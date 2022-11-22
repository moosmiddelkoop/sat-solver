############################
# Important! Literals are unsigned, variables are signed
# Literals and variables are represented as integers
# Therefore clauses are lists of integers
############################

import numpy as np
from collections import Counter
from copy import deepcopy
import time

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
    # clauses_copy = clauses.copy()

    # Eliminates clauses that containt the variable
    # clauses_copy = [clause for clause in clauses if variable not in clause]

    for clause in clauses:
        if variable in clause:
            clauses_copy.remove(clause)

    # Eliminates literals from clauses when the negative literal is included
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

    i = 0
    # contradiction/UNSAT if any empty clause is included in the knowledge base
    for clause in clauses:
        i += 1
        if len(clause) == 0:
            return False

    # if len([clause for clause in clauses if len(clause) == 0]) >= 1:
    #     return False
    
    else:
        return None

### CHECK WHERE BEST TO PLACE SUDOKU SIZE
def solve(clauses, var_dict, backtracks, heuristic = None, sudoku_size = 9, depth=0):
    """
    Recursive DPLL solver
    """

    # Create deepcopies of clauses and literals up to this point
    temp_clauses = clauses.copy()
    temp_vars = var_dict.copy()
    # temp_clauses = deepcopy(clauses)
    # temp_vars = deepcopy(var_dict)

    # handle unit clauses
    temp_clauses, temp_vars = handle_unit(temp_clauses, temp_vars)

    satisfiable = check_result(temp_clauses)
    if satisfiable != None: 
        return satisfiable, temp_vars, backtracks
    
    # Threshold for human heuristic: if more than 60% of Sudoku filled, do not apply heuristic
    if heuristic == 'human':
        no_true_literals = len([k for k,v in temp_vars.items() if v == True])
        if no_true_literals > (sudoku_size ** 2) * 0.7:
            heuristic = None
    
    if heuristic == None:
        # Extract key of first literal that == None
        next_literal = [k for (k, v) in temp_vars.items() if v == None][0]
        # First: for literal = FALSE
        temp_vars[next_literal] = False # Truth Assignment
        variable = -next_literal
        false_clauses = simplify_clauses(temp_clauses, variable)
        result = solve(false_clauses, temp_vars, backtracks, heuristic, sudoku_size, depth=depth+1)
        if(result[0]): 
            temp_clauses = false_clauses
            return result

        #Then: try literal = True
        backtracks += 1
        temp_vars[next_literal] = True
        variable = next_literal
        temp_clauses = simplify_clauses(temp_clauses, variable)
        return solve(temp_clauses, temp_vars, backtracks, heuristic, sudoku_size, depth=depth+1)

    #After handling unit clause, apply heuristics
    elif heuristic == 'human':
        
        key, assignment = human_heuristic(temp_vars, sudoku_size)
        temp_vars[key] = assignment
        variable = key if assignment else -key
        false_clauses = simplify_clauses(temp_clauses, variable)
        result = solve(false_clauses, temp_vars, backtracks, heuristic, sudoku_size)
        if(result[0]): 
            temp_clauses = false_clauses
            return result
    
        # Then: Try opposite
        backtracks += 1
        temp_vars[key] = False if assignment else True # Truth Assignment
        variable = -key if assignment else key
        temp_clauses = simplify_clauses(temp_clauses, variable)
        return solve(temp_clauses, temp_vars, backtracks, heuristic, sudoku_size)

    elif heuristic == 'DLCS':
        candidate_vars = [k for (k, v) in temp_vars.items() if v == None]
        key, assignment = dlcs_heuristic(temp_clauses, candidate_vars)
        temp_vars[key] = assignment
        variable = key if assignment else -key
        false_clauses = simplify_clauses(temp_clauses, variable)
        result = solve(false_clauses, temp_vars, backtracks, heuristic, sudoku_size)
        if(result[0]): 
            temp_clauses = false_clauses
            return result
    
        # Then: Try opposite
        backtracks += 1
        temp_vars[key] = False if assignment else True # Truth Assignment
        variable = -key if assignment else key
        temp_clauses = simplify_clauses(temp_clauses, variable)
        return solve(temp_clauses, temp_vars, backtracks, heuristic, sudoku_size)


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
    
    
def dpll(clauses, heuristic=None):
    '''
    MASTER FUNCTION
    '''
    # get variable dict
    variables = get_vars(clauses)   

    # Get sudoku size (max number of rows as proxy): Needed for human heuristic
    sudoku_size = max(int(str(item)[0]) for item in list(variables.keys()))
    
    # check if problem is already solved 
    # TODO: fix this
    satisfiable = check_result(clauses)
    if satisfiable != None: 
        return satisfiable, variables

    backtracks = 0
    
    # solve it
    return solve(clauses, variables, backtracks, heuristic, sudoku_size)


def dlcs_heuristic(clauses, vars):

    '''DLCS Heuristic'''

    count_dict = {}
    pos_count, neg_count = 0,0
    for clause in clauses:
        for l in vars:
            if l in clause: pos_count += 1
            if -l in clause: neg_count += 1
            total_count = pos_count + neg_count
            count_dict.update({l: [total_count, pos_count, neg_count]})

        max_count = max([value[0] for value in count_dict.values()])
        max_key = [key for key, value in count_dict.items() if value[0] == max_count][0]
        
        #Assignment:
        assignment = True if count_dict[max_key][1] > count_dict[max_key][2] else False
        
        return max_key, assignment


def human_heuristic(vars_dict, sudoku_size):
    
    row_count, col_count, square_count = [],[],[]

    # Check literals that arae assigned True:

    true_literals = []
    for key, value in vars_dict.items():
        if value == True:
            true_literals.append(key)

    for literal in true_literals:
        row, col = int(str(literal)[0]), int(str(literal)[1])
        row_count.append(row)
        col_count.append(col)
        
        # Square count:
        if sudoku_size == 16:
            
            if row < 5 and col < 5:
                square = 1
            elif row < 5 and col > 4 and col < 9:
                square = 2
            elif row < 5 and col > 8 and col < 13:
                square = 3
            elif row < 5 and col > 12:
                square = 4
                
            if row > 4 and row < 9 and col < 5:
                square = 5
            elif row > 4 and row < 9 and col > 4 and col < 9:
                square = 6
            elif row > 4 and row < 9 and col > 8 and col < 13:
                square = 7
            elif row > 4 and row < 9 and col > 12:
                square = 8
                
            if row > 8 and row < 13 and col < 5:
                square = 9
            elif row > 8 and row < 13 and col > 4 and col < 9:
                square = 10
            elif row > 8 and row < 13 and col > 8 and col < 13:
                square = 11
            elif row > 8 and row < 13 and col > 12:
                square = 12
                
            if row > 12 and col < 5:
                square = 13
            elif row > 12 and col > 4 and col < 9:
                square = 14
            elif row > 12 and col > 8 and col < 13:
                square = 15
            elif row > 12 and col > 12:
                square = 16
                
                
        elif sudoku_size == 9:
            
            if row < 4 and col < 4:
                square = 1
            elif row < 4 and col > 3 and col < 7:
                square = 2
            elif row < 4 and col > 6:
                square = 3
            elif row > 3 and row < 7 and col < 4:
                square = 4
            elif row > 3 and row < 7 and col > 3 and col < 7:
                square = 5
            elif row > 3 and row < 7 and col > 6:
                square = 6
            elif row > 6 and col < 4:
                square = 7
            elif row > 6 and col > 3 and col < 7:
                square = 8
            elif row > 6 and col > 6:
                square = 9
        
        elif sudoku_size == 4:
            
            if row < 3 and col < 3:
                square = 1
            if row < 3 and col > 2:
                square = 2
            if row > 2 and col < 3:
                square = 3
            elif row > 2 and col > 2:
                square = 4
        
        
        square_count.append(square)
            
    row_count_dict = Counter(row_count)
    col_count_dict = Counter(col_count)
    square_count_dict = Counter(square_count)
    
    # Excluding all rows, columns and squares that are already filled (when number of occurences == sudoku size) 
    row_count_dict_clean= {k: v for k, v in row_count_dict.items() if v != sudoku_size}
    col_count_dict_clean = {k: v for k, v in col_count_dict.items() if v != sudoku_size}
    square_count_dict_clean = {k: v for k, v in square_count_dict.items() if v != sudoku_size}

    # 
    max_occurence_dict = {"row" + str(max(row_count_dict_clean, key=row_count_dict_clean.get)): max(row_count_dict_clean.values()),
                         "col" + str(max(col_count_dict_clean, key=col_count_dict_clean.get)): max(col_count_dict_clean.values()),
                        "sq." + str(max(square_count_dict_clean, key=square_count_dict_clean.get)): max(square_count_dict_clean.values())}

    # Get key of entry in the dictionary that has the highest count. If two have the same, choose one randomly (that's done in the second line)
    chosen_start = [k for k,v in max_occurence_dict.items() if v == max(max_occurence_dict.values())]
    chosen_start = chosen_start[np.random.randint(len(chosen_start))] if len(chosen_start) > 1 else chosen_start[0]
    
    available_literals = [key for key, val in vars_dict.items() if val == None]

    if chosen_start[:3] == "row":
        candidate_literals = [i for i in available_literals if int(str(i)[0]) == int(chosen_start[3:])]
        
    elif chosen_start[:3] == "col":
        candidate_literals = [i for i in available_literals if int(str(i)[1]) == int(chosen_start[3:])]
        
    elif chosen_start[:3] == "sq.":
        square_no = int(chosen_start[3:])
        
        if sudoku_size == 16:
            if square_no in (1,5,9,13):
                lower_col_boundary = 0
                upper_col_boundary = 5
            
            if square_no in (2,6,10,14):
                lower_col_boundary = 4
                upper_col_boundary = 9
            
            if square_no in (3,7,11,15):
                lower_col_boundary = 8
                upper_col_boundary = 13
            
            if square_no in (4,8,12,16):
                lower_col_boundary = 12
                upper_col_boundary = 17
            
            if square_no in (1,2,3,4):
                lower_row_boundary = 0
                upper_row_boundary = 5
            
            if square_no in (5,6,7,8):
                lower_row_boundary = 4
                upper_row_boundary = 9
            
            if square_no in (9,10,11,12):
                lower_row_boundary = 8
                upper_row_boundary = 13
            
            if square_no in (13,14,15,16):
                lower_row_boundary = 12
                upper_row_boundary = 17
                
        if sudoku_size == 9:
            if square_no in (1,4,7):
                lower_col_boundary = 0
                upper_col_boundary = 4
            
            if square_no in (2,5,8):
                lower_col_boundary = 3
                upper_col_boundary = 7
            
            if square_no in (3,6,9):
                lower_col_boundary = 6
                upper_col_boundary = 10
            
            if square_no in (1,2,3):
                lower_row_boundary = 0
                upper_row_boundary = 4
            
            if square_no in (4,5,6):
                lower_row_boundary = 3
                upper_row_boundary = 7
            
            if square_no in (7,8,9):
                lower_row_boundary = 6
                upper_row_boundary = 10
        
        elif sudoku_size == 4:
            if square_no == 1:
                lower_col_boundary = 0
                upper_col_boundary = 3
                lower_row_boundary = 0
                upper_row_boundary = 3
            
            if square_no == 2:
                lower_col_boundary = 2
                upper_col_boundary = 5
                lower_row_boundary = 0
                upper_row_boundary = 3
            
            if square_no == 3:
                lower_col_boundary = 0
                upper_col_boundary = 3
                lower_row_boundary = 2
                upper_row_boundary = 5
            
            if square_no == 4:
                lower_col_boundary = 2
                upper_col_boundary = 5
                lower_row_boundary = 2
                upper_row_boundary = 5
            
        candidate_literals = [i for i in available_literals if int(str(i)[0]) > lower_row_boundary and int(str(i)[0]) < upper_row_boundary and int(str(i)[1]) > lower_col_boundary and int(str(i)[1]) < upper_col_boundary]
            
    # Choose a random literal from all candidate literals and assign True to it
    literal = candidate_literals[np.random.randint(len(candidate_literals))]
    assignment = True
    
    return literal, assignment
        



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
    # clauses = [[-4, 5], [-5, 4], [-4, -5], [4, 5], [1, 3, 2], [3, -2, -1]]

    #print(dpll(clauses))