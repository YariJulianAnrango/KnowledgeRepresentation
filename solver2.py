import random
import numpy as np
import copy
clauses = [[111,121,-131],[121,131],[-121],[-111,131]]
all_elements = [abs(x) for l in clauses for x in l]
a = np.array(all_elements)
unique = np.unique(a)
unique_elements = list(unique)

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

def test_all_clauses(clauses, trues, falses,n_elements):
    n_succes = 0
    for clause in clauses:
        if testclause(clause, trues, falses) == 1:
            n_succes += 1
        elif testclause(clause, trues, falses) == 0:
            n_succes += 0
    if n_succes == len(clauses):
        result = True
    elif n_elements == len(trues) + len(falses) and n_succes < len(clauses):
        result = False
    else:
        result = -1
    return result



trues = []
falses = []
def dpll_1(clauses,unique_elements):
    global trues, falses
    element_copy = copy.deepcopy(unique_elements)
    n_elements = len(element_copy)
    print('clauses',clauses)
    print('unique_elements',unique_elements)
    print(trues, falses)
    input()
    if len(unique_elements) != 0:
        e = random.choice(unique_elements)
        unique_elements.remove(e)
        falses += [abs(e)]
    if test_all_clauses(clauses, trues, falses, n_elements) == False:
        print('hey')
        print(trues, falses)
        return False
    if test_all_clauses(clauses, trues, falses, n_elements) == True:
        print(trues, falses)
        print('Solved!1')
        return True
    print('xxxxxxxxxxxxxxxxxxxxxxxmark')
    if dpll_1(clauses, unique_elements):
        print('Solved!2')
        return True
    else:
        print('trues and falses', trues, falses)
        falses.remove(abs(e))
        trues += [abs(e)]
        print('trues and falses', trues, falses)
        return dpll_1(clauses, unique_elements)

#print(dpll_1(clauses, unique_elements))