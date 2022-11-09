def read(self):
    '''Method for reading the clauses from the input file.

    Returns:
        list -- list of clauses
    '''

    # Initialize clauses list.
    clauses = []

    # Initialize variables.
    vars_tmp = set()

    # Start reading from the file.
    with open(self.file, 'r') as input_file: #opens the file for reading
        for line in input_file: #for every line in the input file
            parsed = line.split() #function that splits the line by every element (between the spaces)

            # Check whether it is valid line or supplementary line.
            if not parsed or parsed[0] == 'p' or parsed[0] == 'c': #if the element starts with p or c
                continue
            else:
                eff_parsed = parsed[:-1] #-1 means splitting on the last item (which is the 0)
                clause = set() #creates an empty set, which will be the clauses
                for lit in eff_parsed: #goes through every item in the line
                    lit = int(lit) #makes the lit a integer
                    clause.add(lit) #adds every item as a integer to the clause

                    # Collect variable.
                    abs_lit = abs(lit)
                    vars_tmp.add(abs_lit)
                clauses.append(list(clause))

    # Initialize all collected variables, e.g. {'115': [False] ...} - where [truth_val]
    self.vars = dict.fromkeys(vars_tmp, False)
    return clauses

read("sudoku-rules-9x9.txt")