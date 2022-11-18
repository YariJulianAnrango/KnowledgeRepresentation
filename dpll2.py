import random
import numpy as np


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
            if clause[0] > 0:
                if abs(clause[0]) not in trues:
                    trues += [abs(clause[0])]
            elif clause[0] < 0:
                if abs(clause[0]) not in falses:
                    falses += [abs(clause[0])]
            clauses.remove(clause)
            removed = True
    if removed:
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
                falses += [false]
    if len(pure_trues) > 0:
        for true in pure_trues:
            if true not in trues:
                trues += [true]
    if len(pure_trues) > 0 or len(pure_trues) > 0:
        return clauses, trues, falses
    else:
        return False

def remove_lit(clauses, trues, falses):
    remove_clause = []
    for clause in clauses:
        remove_literal = []
        for l in clause:
            if l < 0 and abs(l) in falses:
                remove_clause += [clause]
                break
            elif l > 0 and l in trues:
                remove_clause += [clause]
                break
            if l < 0 and abs(l) in trues:
                remove_literal += [l]
            elif l > 0 and l in falses:
                remove_literal += [l]
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
