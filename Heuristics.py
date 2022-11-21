from itertools import chain

def Jeroslow_Wang(clauses, trues, falses):
    J = defaultdict(int)
    for clause in clauses:
        lengthclause = len(clause)
        for l in clause:
            J[l] += 2 ** (-lengthclause)

        maxpair = [-1, 0]
        for k in J.keys():
            sum_J = J[k] + J[-k]
            if sum_J > maxpair[1] and maxpair[0] != -k:
                maxpair = [k, sum_J]

        split = abs(maxpair[0])
        if J[split] >= J[-split]:
            return split
        else:
            return -split


def DLIS(clauses):
    cp = defaultdict(int)
    cn = defaultdict(int)
    for clause in clauses:
        for l in clause:
            if l > 0:
                cp[l] += 1
            if l < 0:
                cn[l] += 1

    maxpaircp = [0, -1]
    for k, v in cp.items():
        if v > maxpaircp[1]:
            maxpaircp = [k, v]

    maxpaircn = [0, -1]
    for k, v in cn.items():
        if v > maxpaircn[1]:
            maxpaircn = [k, v]

    if maxpaircn[1] > maxpaircp[1]:
        return maxpaircp[0]
    else:
        return maxpaircn[0]


def DLCS(clauses):
    cp = defaultdict(int)
    cn = defaultdict(int)
    for clause in clauses:
        for l in clause:
            if l > 0:
                cp[l] += 1
            if l < 0:
                cn[l] += 1

    largest_sum = 0
    combined = chain(cp, cn)
    for l in combined:
        if cp[l] + cn[l] > largest_sum:
            largest_sum = cp[l] + cn[l]
            lit = l

    if cp[lit] > cn[lit]:
        return cp[lit]
    else:
        return cn[lit]

a = [1,2,3]
def MOMs(clauses):
    smallest_clause = len(clauses[0])
    for clause in clauses:
        if len(clause) < smallest_clause:
            smallest_clause = len(clause)

    # smallest_clause = min(len(clauses)) <-- weet niet of dit zo kort kan?

    shortest_clauses = []
    highest_occ = 0
    number = dict()
    for clause in clauses:
        if len(clause) == smallest_clause:
            for l in clause:
                number[l] = number.get(l, 0) + 1
    for l in number.keys():
        function = (number[l] + number.get(-l, 0)) * 2 ** k + number[l] * number.get(-l, 0)
        if function > highest_occ:
            highest_occ = function
            lit = l
    return lit