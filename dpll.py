
test_input = [[1, 2, 3], [1, -2], [1, -3], [-2, 3]]
literals = [1, 2, 3]


found_literals = []

def solver2(clauses, literal):

    global found_literals
    temp_clauses = clauses.deepcopy()

    for clause in temp_clauses:

        if literal in clause:
                temp_clauses.remove(clause)
            
        elif -literal in clause:
                clause.remove(literal)

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


solver2()


