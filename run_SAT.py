import time
import copy

from dpll2 import empty_clause
from dpll2 import tautology
from dpll2 import unit_clause
from dpll2 import pure_literal
from dpll2 import remove_lit
from dpll2 import draw_literal
from Testing import test_all_clauses
from translate_sudokus import load_cnfs
from Reading import read_dimacs
import Heuristics as hs


def dpll2():
    global trues, falses, sol_t, sol_f, clauses, backtracks, l, split_on, split

    # Removing clauses and literals
    clauses, trues, falses = remove_lit(clauses, trues, falses)

    # Succes
    if len(clauses) == 0:
        sol_t = trues
        sol_f = falses
        return True

    # Failed
    if empty_clause(clauses):
        sol_t = trues
        sol_f = falses
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

    # Remove clauses and literals
    clauses, trues, falses = remove_lit(clauses, trues, falses)

    if len(clauses) > 0:
        # Choose where to split
        if split == 'random':
            l = draw_literal(clauses, trues, falses)

            if l not in trues and l not in falses:
                trues += [l]
                split_on += [l]

        if split == 'MOMs':
            l = hs.MOMs(clauses)

            if l not in trues and l not in falses:
                trues += [l]
                split_on += [l]
        if split == 'DLCS':
            l = hs.DLCS(clauses)

            if l < 0:
                if l not in falses and l not in trues:
                    falses += [abs(l)]
                    split_on += [abs(l)]
            elif l > 0:
                if l not in falses and l not in trues:
                    trues += [abs(l)]
                    split_on += [abs(l)]
        if split == 'DLIS':
            l = hs.DLIS(clauses)

            if l < 0:
                if l not in falses and l not in trues:
                    falses += [abs(l)]
                    split_on += [abs(l)]
            elif l > 0:
                if l not in falses and l not in trues:
                    trues += [abs(l)]
                    split_on += [abs(l)]

        if split == 'JW':
            l = hs.Jeroslow_Wang(clauses)

            if l < 0:
                if l not in falses and l not in trues:
                    falses += [abs(l)]
                    split_on += [abs(l)]
            elif l > 0:
                if l not in falses and l not in trues:
                    trues += [abs(l)]
                    split_on += [abs(l)]


    # Make copies
    backtrack_clauses = copy.deepcopy(clauses)
    backtrack_trues = copy.deepcopy(trues)
    backtrack_falses = copy.deepcopy(falses)

    if dpll2():
        return True
    else:
        # Backtracking
        if len(split_on) > 0:
            rem = split_on[-1]
            split_on.remove(rem)

            clauses = backtrack_clauses
            trues = backtrack_trues
            falses = backtrack_falses


            if rem in trues:
                trues.remove(rem)
                if rem not in falses:
                    falses += [rem]
            elif rem in falses:
                falses.remove(rem)
                if rem not in trues:
                    trues += [rem]

        backtracks += 1

        dpll2()



# Run sudokus
st = time.time()
sudokus = load_cnfs('./sudokus/1000 sudokus.txt')
Results = []
weird_trues = []
weird_falses = []
Results_falses = []
tries = 0
split = 'JW' # Choose heuristic
for sudoku in sudokus[:10]: # Change 'sudokus' to 'sudokus[:x]' to run x amount of sudokus
    sudoku_time = time.time()
    print('new sudoku')
    clauses = read_dimacs(sudoku)
    clauses = [[int(j) for j in i] for i in clauses]
    og_clauses = copy.deepcopy(clauses)

    split_on = []
    backtracks = 0
    trues = []
    falses = []
    sol_t = []
    sol_f = []
    dpll2()

    while test_all_clauses(og_clauses, sol_t, sol_f) == False and tries < 100:
        print('retrying')
        split_on = []
        backtracks = 0
        trues = []
        falses = []
        sol_t = []
        sol_f = []
        clauses = copy.deepcopy(og_clauses)
        dpll2()
        Results_falses += [[False, len(sol_f), backtracks]]
        weird_trues += [sol_t]
        weird_falses += [sol_f]
        tries += 1
    if test_all_clauses(og_clauses, sol_t, sol_f) and len(sol_t) == 81 or tries < 100:
        Results += [[True, len(sol_t), backtracks, tries]]
    else:
        Results += [[False, len(sol_t), backtracks, tries]]

    sudoku_end = time.time()
    print('Execution time this sudoku:', sudoku_end-sudoku_time, 'seconds')
    print()


et = time.time()

# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')
