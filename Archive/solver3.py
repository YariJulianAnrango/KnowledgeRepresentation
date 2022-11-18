import random
import numpy as np
from Reading import read
from datetime import datetime

clauses = read('sudoku2.cnf')
#clauses = [[111,121,131],[111,-131],[-121],[-111,131]]
all_elements = [abs(x) for l in clauses for x in l]
a = np.array(all_elements)
unique = np.unique(a)
unique_elements = list(unique)

def testclause(clause, trues, falses):
    notin = 0
    v = 0
    for i in range(len(clause)):
        if abs(clause[i]) not in trues and abs(clause[i]) not in falses:
            notin += 1
            continue
        if abs(clause[i]) in trues and clause[i] > 0:
            v += 1
        elif abs(clause[i]) in falses and clause[i] < 0:
            v += 1
    if notin > 0:
        return -1
    elif v > 0:
        return True
    elif v == 0:
        return False


def test_all_clauses(clauses, trues, falses):
    notyet = 0
    for clause in clauses:
        if testclause(clause, trues, falses) == -1:
            notyet += 1
        elif testclause(clause, trues, falses) == False:
            return False
    if notyet > 0:
        return 'Not yet'
    #print('notyet',notyet, 'len clauses',len(clauses))
    return True

trues = []
falses = []
def dpll(clauses, unique_elements, pas):
    global trues, falses
    print('trues',trues,'falses',falses)
    if test_all_clauses(clauses, trues, falses) == False:
        if pas in trues:
            trues.remove(pas)
            falses += [pas]
            print('trues',trues,'falses',falses)
        return False
    if test_all_clauses(clauses, trues, falses) == True:
        print(trues, falses)
        print('test 2')
        return True
    pa = random.choice(unique_elements)
    while pa in falses or pa in trues:
        pa = random.choice(unique_elements)
    falses += [pa]
    if dpll(clauses, unique_elements, pa):
        return True
    else:
        index = falses.index(pa)
        falses = falses[:index]
        trues += [pa]
        return dpll(clauses, unique_elements, pa)


print(dpll(clauses, unique_elements, 0))