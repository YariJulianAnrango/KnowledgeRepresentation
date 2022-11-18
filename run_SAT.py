import time
import copy
import random
import numpy as np

from matrix_convert import print_as_matrix
from dpll2 import empty_clause
from dpll2 import tautology
from dpll2 import unit_clause
from dpll2 import pure_literal
from dpll2 import remove_lit
from dpll2 import draw_literal
from Testing import test_all_clauses
from translate_sudokus import load_cnfs
from Reading import read_dimacs


def dpll2():
    global trues, falses, sol_t, sol_f, og_clauses, clauses, backtracks, l

    # Removing clauses and literals
    clauses, trues, falses = remove_lit(clauses, trues, falses)

    # Succes
    if len(clauses) == 0:
        print('done')
        print(trues)
        sol_t = trues
        sol_f = falses
        return True

    # Failed
    if empty_clause(clauses):
        return False

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

    l = draw_literal(clauses, trues, falses)

    if l not in trues and l not in falses:
        trues += [l]
    print('l in trues',l)
    if dpll2():
        return trues, falses
    else:
        print('l',l)
        print('trues', np.sort(np.array(trues)))
        while l in trues:
            trues.remove(l)
        if l not in falses:
            falses += [l]
        backtracks += 1
        print('trues after removal',np.sort(np.array(trues)))
        print()
        dpll2()



# Run 10 sudokus
st = time.time()
sudokus = load_cnfs('./sudokus/1000 sudokus.txt')
Results = []
weird_trues = []
Results_falses = []
for sudoku in sudokus[:5]:
    sudoku_time = time.time()
    print('new sudoku')
    clauses = read_dimacs(sudoku)
    clauses = [[int(j) for j in i] for i in clauses]
    og_clauses = copy.deepcopy(clauses)

    backtracks = 0
    trues = []
    falses = []
    sol_t = []
    sol_f = []
    dpll2()
    print(backtracks)

    if test_all_clauses(og_clauses, trues, sol_f):
        #print(sol_t)
        Results += [[True,len(sol_t), backtracks]]
        Results_falses += [[True, len(sol_f),backtracks]]
    else:
        #print('oh oh')
        #print(sol_t)
        Results += [[False, len(trues),backtracks]]
        Results_falses += [[False, len(sol_f), backtracks]]

    if len(sol_t) != 81:
        #print('not 81', len(sol_t))
        weird_trues += [sol_t]
    sudoku_end = time.time()
    print('Execution time:', sudoku_end-sudoku_time, 'seconds')
    print()


et = time.time()

# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')


print_as_matrix(Trues = [129, 171, 357, 392, 451, 532, 686, 774, 897, 943, 998, 134, 366, 523, 755, 936, 183, 642, 964, 428, 868, 117, 226, 212, 196, 876, 927, 793, 746, 556, 767, 416, 841, 261, 162, 158, 253, 145, 548, 654, 514, 447, 678, 824, 637, 473, 722, 663, 482, 972, 959, 494, 852, 611, 321, 625, 915, 439, 731, 699, 981, 591, 295, 465, 789, 569, 885, 718, 833, 238, 313, 379, 335, 819, 575, 277, 344, 587, 249, 388, 284])

