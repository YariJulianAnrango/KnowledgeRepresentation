import copy
import random
import numpy as np
from Testing import test_all_clauses
from translate_sudokus import load_cnfs
from Reading import read_dimacs

sudokus = load_cnfs('./sudokus/1000 sudokus.txt')
clauses = read_dimacs(sudokus[0])
clauses = [[int(j) for j in i] for i in clauses]
og_clauses = copy.deepcopy(clauses)

def empty_clause(clauses):
    for clause in clauses:
        if len(clause) == 0:
            return True
    return False

def tautology(clauses, trues, falses):
    removed = False
    for clause in clauses:
        for l in clause:
            if l in clause and -l in clause:
                clauses.remove(clause)
                removed = True
    if removed:
        return clauses, trues, falses
    else:
        return False


def unit_clause(clauses, trues, falses):
    removed = False
    for clause in clauses:
        if len(clause) == 1:
            print('unit clause', clause)
            if clause[0] > 0:
                if abs(clause[0]) not in trues:
                    trues += [abs(clause[0])]
            elif clause[0] < 0:
                if abs(clause[0]) not in falses:
                    falses += [abs(clause[0])]
            clauses.remove(clause)
            removed = True
    if removed:
        print('unit_clause removed')
        print()
        return clauses, trues, falses
    else:
        return False

def pure_literal(clauses, trues, falses):
    not_pure = []
    pure_falses = []
    pure_trues = []
    for clause in clauses:
        for l in clause:
            if l < 0 and abs(l) in pure_trues:
                pure_trues.remove(abs(l))
                not_pure += [abs(l)]
            elif l > 0 and l in pure_falses:
                pure_falses.remove(l)
                not_pure += [abs(l)]
            elif l < 0 and abs(l) not in pure_falses and abs(l) not in not_pure and abs(l) not in trues:
                pure_falses += [abs(l)]
            elif l > 0 and l not in pure_trues and l not in not_pure and l not in falses:
                pure_trues += [l]
    if len(pure_falses) > 0:
        for false in pure_falses:
            if false not in falses:
                print('putting in falses after pure literal')
                print('pure false',false)
                falses += [false]
    if len(pure_trues) > 0:
        for true in pure_trues:
            if true not in trues:
                print('putting in trues after pure true')
                print('pure true',true)
                trues += [true]
    if len(pure_trues) > 0 or len(pure_trues) > 0:
        return clauses, trues, falses
    else:
        return False

def remove_lit(clauses, trues, falses):
    remove_clause = []
    for clause in clauses:
        remove_literal = []
        print('working on clause',clause)
        for l in clause:
            if l < 0 and abs(l) in falses:
                #clauses.remove(clause)
                remove_clause += [clause]
                print('clause ',clause,' removed')
                break
            elif l > 0 and l in trues:
                remove_clause += [clause]
                #clauses.remove(clause)
                print('clause ', clause, ' removed')
                break
            if l < 0 and abs(l) in trues:
                remove_literal += [l]
                print('literal ', l, ' removed')
                #clause.remove(l)
            elif l > 0 and l in falses:
                remove_literal += [l]
                print('literal ', l, ' removed')
                #clause.remove(l)
        if len(remove_literal) > 0:
            for l in remove_literal:
                clause.remove(l)
    if len(remove_clause) > 0:
        for clause in remove_clause:
            clauses.remove(clause)
    return clauses, trues, falses

def draw_literal(clauses, trues, falses):
    elements = [abs(x) for l in clauses for x in l] + trues + falses

    all_elements = elements + trues + falses
    a = np.array(all_elements)
    unique = np.unique(a)
    unique_elements = list(unique)
    l = random.choice(unique_elements)
    trues_falses = np.array(trues + falses)
    unique_trues_falses = np.unique(trues_falses)
    unique_trues_falses = list(unique_trues_falses)

    if len(unique_elements) > len(unique_trues_falses):
        while l in trues or l in falses:
            l = random.choice(unique_elements)
    return l

def dpll2():
    global trues, falses, sol_t, sol_f, og_clauses, clauses
    print('new cycle')
    print(clauses)
    print(trues)
    print(falses)
    print()

    # Removing clauses and literals
    clauses, trues, falses = remove_lit(clauses, trues, falses)

    # Succes
    if len(clauses) == 0:
        print(trues)
        print(falses)
        sol_t = trues
        sol_f = falses
        return True

    # Failed
    if empty_clause(clauses):
        print('retrying')
        trues = []
        falses = []
        clauses = copy.deepcopy(og_clauses)
        return clauses, trues, falses

    # Tautology
    taut = tautology(clauses, trues, falses)
    if taut != False:
        clauses, trues, falses = taut
        dpll2()

    # Unit clause
    unit = unit_clause(clauses, trues, falses)
    if unit != False:
        clauses, trues, falses = unit
        dpll2()

    # Pure literal
    pure = pure_literal(clauses, trues, falses)
    if pure != False:
        clauses, trues, falses = pure
        dpll2()


    print('After removal')
    print(clauses)
    print(trues)
    print(falses)

    l = draw_literal(clauses, trues, falses)
    print('l',l)
    print()
    if l not in trues and l not in falses:
        trues += [l]
    if dpll2():
        return trues, falses
    else:
        while l in trues:
            trues.remove(l)
        if l not in falses:
            falses += [l]
        dpll2()


sudokus = load_cnfs('./sudokus/1000 sudokus.txt')

'''
sudoku = read_dimacs(sudokus[1])
clauses = [[int(j) for j in i] for i in sudoku]
og_clauses = copy.deepcopy(clauses)
dpll2()

'''

# Run 10 sudokus
Results = []
for sudoku in sudokus[:10]:
    clauses = read_dimacs(sudoku)
    clauses = [[int(j) for j in i] for i in clauses]
    og_clauses = copy.deepcopy(clauses)
    trues = []
    falses = []
    sol_t = []
    sol_f = []
    dpll2()
    if test_all_clauses(clauses, sol_t, sol_f):
        Results += [True,len(sol_t)]

print(Results)


