import random
import copy

def read(file):
    # Initialize clauses list.
    clauses = []

    # Initialize variables.
    vars_tmp = set()

    # Start reading from the file.
    with open(file, 'r') as input_file: #opens the file for reading
        for line in input_file: #for every line in the input file
            parsed = line.split() #function that splits the line by every element (between the spaces)

            # Check whether it is valid line or supplementary line.
            if not parsed or parsed[0] == 'p' or parsed[0] == 'c': #if the element starts with p or c
                continue
            else:
                eff_parsed = parsed[:-1] #-1 means splitting on the last item (which is the 0)
                clause = set() #creates an empty set, which will be the clauses
                for lit in eff_parsed: #goes through every item in the line
                    lit = int(lit) #makes the list an integer
                    clause.add(lit) #adds every item as a integer to the clause

                    # Collect variable.
                    abs_lit = abs(lit)
                    vars_tmp.add(abs_lit)
                clauses.append(list(clause))

    # Initialize all collected variables, e.g. {'115': [False] ...} - where [truth_val]
    return clauses

def solver(clauses):
    count = 0
    '''Main method of solver.
    Arguments:
        clauses {list} -- list of clauses
    Returns:
        dict -- dictionary of variables with assigned values
    '''

    # print('|START count:', self.count)
    # print('start:', clauses)
    clauses = pure_literals(clauses)
    # print('after pure:', clauses)
    clauses = unit_clauses(clauses)
    # print('after unit:', clauses)
    if [] in clauses:
        # print('false')
        return False
    if len(clauses) == 0:
        print("You have succeed!")
        return vars
    split_var = random.choice(random.choice(clauses))
    count += 1
    # print(split_var)
    tmp = copy.deepcopy(clauses)
    assignment = solver(remove_clauses(split_var, clauses))
    if assignment is False:
        # print('backtracking...')
        count += 1
        clauses = copy.deepcopy(tmp)
        assignment = solver(remove_clauses(-split_var, clauses))
    if assignment is False:
        return False
    return vars

def remove_clauses(split_var, clauses):
    new_clauses = []
    if split_var >= 0:
        vars[split_var] = True
    else:
        vars[abs(split_var)] = False
    for clause in clauses:
        if split_var in clause:
            continue
        else:
            if -split_var in clause:
                clause.remove(-split_var)
            new_clauses.append(clause)
    return new_clauses

def pure_literals(clauses):
    p_lits = set()
    non_p_lits = set()
    for clause in clauses:
        for lit in clause:
            neg_lit = -lit
            abs_lit = abs(lit)
            if neg_lit not in p_lits:
                if abs_lit not in non_p_lits:
                    p_lits.add(lit)
            else:
                p_lits.remove(neg_lit)
                non_p_lits.add(abs_lit)
    for lit in p_lits:
        clauses = remove_clauses(lit, clauses)
    return clauses

def unit_clauses(clauses):
    '''Collect and remove unit clauses from the list of clauses.
            Returns:
                list -- list of clauses
            '''

    unit_var = set()
    for clause in clauses:
        if len(clause) == 1:
            unit_var.add(clause[0])
    while len(unit_var) > 0:
        for unit in unit_var:
            clauses = remove_clauses(unit, clauses)
        unit_var = set()
        clauses = unit_clauses(clauses)
    return clauses

clauses = read('sudoku1.cnf')
solver(clauses)
