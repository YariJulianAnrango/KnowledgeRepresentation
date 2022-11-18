from Reading import read

# To run with sudoku, use clauses = read('sudoku1.cnf')
clauses = [[111,121,131],[111,-121],[111,-131],[-111,131]]

def testclause(clause, trues, falses):
    v = 0
    for i in range(len(clause)):
        if abs(clause[i]) in trues and clause[i] > 0:
            v += 1
        elif abs(clause[i]) in falses and clause[i] < 0:
            v += 1
    if v > 0:
        result = 1
    elif v == 0:
        result = 0
    return result

def test_all_clauses(clauses, trues, falses):
    n_succes = 0
    for clause in clauses:
        if testclause(clause, trues, falses) == 1:
            n_succes += 1
        elif testclause(clause, trues, falses) == 0:
            n_succes += 0
    if n_succes == len(clauses):
        result = True
    else:
        result = False
    return result

def SATsolver(clauses, trues, falses, n_remove = 0):
    for clause in clauses:
        for e in clause:
            if abs(e) not in trues and abs(e) not in falses:
                #print('flipping', e)
                falses += [abs(e)]
                if test_all_clauses(clauses, trues, falses):
                    print('Succes! 1')
                    print('trues after succes1', trues)
                    print('falses after succes1', falses)
                    return trues, falses
                falses.remove(abs(e))
                trues += [abs(e)]
                if test_all_clauses(clauses, trues, falses):
                    print('Succes! 2')
                    print('trues after succes2',trues)
                    print('falses after succes2',falses)
                    return trues, falses
                trues.remove(abs(e))
                falses += [abs(e)]
    if test_all_clauses(clauses, trues, falses):
        print('Succes! 3')
        return trues, falses
    else:
        #print('Clauses not satisfied, making changes')
        if len(trues) != 0:
            falses.insert(-n_remove,trues[-1])
            trues.remove(trues[-1])
        n_remove += 1
        print('n_remove',n_remove)
        print('false',falses)
        print('trues',trues)
        trues += [falses[-n_remove]]
        for i in range(n_remove):
            falses.remove(falses[-1])
        return SATsolver(clauses, trues, falses, n_remove)

trues_list, falses_list = SATsolver(clauses, trues = [], falses = [])



