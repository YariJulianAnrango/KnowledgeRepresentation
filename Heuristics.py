def Jeroslow_Wang(clauses):
    J = dict()
    Jmax = 0
    literal = 0
    for clause in clauses:
        lengthclause = len(clause)
        for l in clause:
            if l not in J.keys():
                J[l] = 2 ** (-lengthclause)
                if J[l] > Jmax:
                    Jmax = J[l]
                    literal = l
            elif l in J.keys():
                J[l] += 2 ** (-lengthclause)
                if J[l] > Jmax:
                    literal = l
        return literal

def DLIS(clauses):
    cp = dict()
    cn = dict()
    for clause in clauses:
        for l in clause:
            if l not in cp:
                if l > 0:
                    cp[l] = 1
                if l < 0:
                    cn[l] = 1
            elif l in cp:
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
    cp = dict()
    cn = dict()
    for clause in clauses:
        for l in clause:
            if l not in cp:
                if l > 0:
                    cp[l] = 1
                if l < 0:
                    cn[l] = 1
            elif l in cp:
                if l > 0:
                    cp[l] += 1
                if l < 0:
                    cn[l] += 1

    largest_sum = 0
    largestpaircp = [0,-1]
    largestpaircn = [0,-1]
    for l in cp.keys():
        if cp[l] + cn[-l] > largest_sum:
            largest_sum = cp[l] + cn[-l]
            largest_cp = cp[l]
            largest_cn = cn[-l]
            largestpaircp = [l,largest_cp]
            largestpaircn = [-l,largest_cn]


    if largestpaircp[1] > largestpaircn[1]:
        return largestpaircp[0]
    else:
        return largestpaircn[0]


def MOMs(clauses):
    smallest_clause = len(clauses[0])

    for clause in clauses:
        if len(clause) < smallest_clause and len(clause) > 0:
            smallest_clause = len(clause)
    cp = dict()
    cn = dict()
    k = 0.5
    highest_occ = 0
    for clause in clauses:
        if len(clause) == smallest_clause:
            for l in clause:
                if l not in cp:
                    if l > 0:
                        cp[l] = 1
                    if l < 0:
                        cn[l] = 1
                elif l in cp:
                    if l > 0:
                        cp[l] += 1
                    if l < 0:
                        cn[l] += 1

    endpair = [0, -1]
    for l in cp.keys():
        if -l in cn:
            ans = (cp[l] + cn[-l]) * (2 ** k) + cp[l] * cn[-l]
        else:
            ans = (cp[l] + 0) * (2 ** k) + cp[l] * 0
        if ans > highest_occ:
            highest_occ = ans
            endpair = [l, ans]

    for l in cn.keys():
        if abs(l) not in cp:
            ans = (0 + cn[l]) * (2 ** k) + 0 * cn[l]
            if ans > highest_occ:
                highest_occ = ans
                endpair = [l, ans]

    if endpair[0] != 0:
        return endpair[0]
    else:
        return False