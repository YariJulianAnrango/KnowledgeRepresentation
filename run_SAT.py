import time
import copy
import random
import numpy as np
import csv
import argparse
from datetime import datetime


from matrix_convert import print_as_matrix
from dpll2 import empty_clause
from dpll2 import tautology
from dpll2 import unit_clause
from dpll2 import pure_literal
from dpll2 import remove_lit
from dpll2 import draw_literal
from Testing import test_all_clauses
from translate_sudokus import load_cnfs
from Reading import read
from Reading import read_sudoku


### Parsing to run in terminal ###
parser = argparse.ArgumentParser(description='Run this script to test the SAT Solver.')
parser.add_argument('-S', metavar='Heuristic', type = int,choices = [1,2,3,4,5],help="Choose an option to pick a Heuristic. -S1 = Random, -S2 = MOM's, -S3 = Jeroslow-Wang, -S4 = DLCS, -S5 = DLIS.")
parser.add_argument('-I', metavar='Input file', type = str, choices = ['sudoku1','sudoku2','sudoku3','sudoku4','sudoku5','1000 sudokus'], help = 'Choose a sudoku to solve.')
args = parser.parse_args()


if args.S == 1:
    split = 'random'
elif args.S == 2:
    split = 'MOMs'
elif args.S == 3:
    split = 'JW'
elif args.S == 4:
    split = 'DLCS'
elif args.S == 5:
    split = 'DLIS'


if args.I == '1000 sudokus':
    multiple_sudokus = load_cnfs('./sudokus/1000 sudokus.txt')
    mul = True

else:
    if args.I == 'sudoku1':
        input = './sudokus/sudoku1.cnf'
    elif args.I == 'sudoku2':
        input = './sudokus/sudoku2.cnf'
    elif args.I == 'sudoku3':
        input = './sudokus/sudoku3.cnf'
    elif args.I == 'sudoku4':
        input = './sudokus/sudoku4.cnf'
    elif args.I == 'sudoku5':
        input = './sudokus/sudoku5.cnf'

    sudoku = read_sudoku(input)
    mul = False

########################


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

    # Choose where to split
    if split == 'random':
        l = draw_literal(clauses, trues, falses)

        if l not in trues and l not in falses:
            trues += [l]
            split_on += [l]
    if split == 'MOMs':
        l = MOMs(clauses)

        if l not in trues and l not in falses:
            trues += [l]
            split_on += [l]
    if split == 'DLCS':
        l = DLCS(clauses)

        if l < 0:
            if l not in falses and l not in trues:
                falses += [abs(l)]
                split_on += [abs(l)]
        elif l > 0:
            if l not in falses and l not in trues:
                trues += [abs(l)]
                split_on += [abs(l)]
    if split == 'DLIS':
        l = DLIS(clauses)

        if l < 0:
            if l not in falses and l not in trues:
                falses += [abs(l)]
                split_on += [abs(l)]
        elif l > 0:
            if l not in falses and l not in trues:
                trues += [abs(l)]
                split_on += [abs(l)]
    if split == 'Jeroslow Wang':
        l = Jeroslow_Wang(clauses)

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
        backtracks += 1

        dpll2()


if mul:
    st = time.time()
    sudokus = copy.deepcopy(multiple_sudokus)
    Results = []
    weird_trues = []
    weird_falses = []
    Results_falses = []
    for sudoku in sudokus[:1]: # Change 'sudokus' to 'sudokus[:x]' to run x amount of sudokus
        sudoku_time = time.time()
        print('New sudoku')
        clauses = read_sudoku(sudoku)
        clauses = [[int(j) for j in i] for i in clauses]
        og_clauses = copy.deepcopy(clauses)

        split_on = []
        backtracks = 0
        trues = []
        falses = []
        sol_t = []
        sol_f = []
        tries = 0
        dpll2()

        while test_all_clauses(og_clauses, sol_t, sol_f) == False:
            tries += 1
            print('Having trouble with this one, retrying...')
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

        sudoku_end = time.time()
        t = sudoku_end - sudoku_time
        if test_all_clauses(og_clauses, sol_t, sol_f) and len(sol_t) == 81:
            Results += [[True, len(sol_t), backtracks, t]]

        print('Execution time this sudoku:', t, 'seconds')
        print()

    et = time.time()
    cols = ['Result', 'length_sol', 'n_backtracks', 'time']


    # datetime object containing current date and time
    now = datetime.now()

    # dd/mm/YY H:M:S
    dt_string = now.strftime("%H:%M")
    with open('results_'+ dt_string + '_' + split + '.csv', 'w') as f:

        write = csv.writer(f)
        write.writerow(cols)
        write.writerows(Results)

    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')
    print(Results)

elif not mul:

    Results = []
    weird_trues = []
    weird_falses = []
    Results_falses = []
    tries = 0
    sudoku_time = time.time()
    print('New sudoku')
    clauses = sudoku
    clauses = [[int(j) for j in i] for i in clauses]
    og_clauses = copy.deepcopy(clauses)

    split_on = []
    backtracks = 0
    trues = []
    falses = []
    sol_t = []
    sol_f = []
    dpll2()

    while test_all_clauses(og_clauses, sol_t, sol_f) == False:
        print('Having trouble with this one, retrying...')
        split_on = []
        backtracks = 0
        trues = []
        falses = []
        sol_t = []
        sol_f = []
        clauses = copy.deepcopy(og_clauses)
        tries += 1
        dpll2()
        Results_falses += [[False, len(sol_f), backtracks]]
        weird_trues += [sol_t]
        weird_falses += [sol_f]

    sudoku_end = time.time()
    t = sudoku_end - sudoku_time
    if test_all_clauses(og_clauses, sol_t, sol_f) and len(sol_t) == 81:
        Results += [[True, len(sol_t), backtracks, t]]

    now = datetime.now()

    cols = ['Result', 'length_sol', 'n_backtracks', 'time']

    dt_string = now.strftime("%H:%M")
    with open('results_' + dt_string + '_' + split + '.csv', 'w') as f:

        write = csv.writer(f)
        write.writerow(cols)
        write.writerows(Results)

    print('Execution time this sudoku:', t, 'seconds')
    print()

else:
    print('Oh oh')
