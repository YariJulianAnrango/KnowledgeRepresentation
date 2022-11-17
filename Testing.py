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
            print(clause)
            notyet += 1
        elif testclause(clause, trues, falses) == False:
            return False
    if notyet > 0:
        return 'Not yet'
    return True