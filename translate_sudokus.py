from math import sqrt

def read_cnf_file(path):

    with open(path, "r") as file_:
        sudokus = file_.read().splitlines()
    amount = int(sqrt(len(sudokus[0])))

    with open("./rules/sudoku-rules-"+str(amount)+"x"+str(amount)+".txt", "r") as file_:
        rules = file_.read().splitlines()[1:]

    encoded_sudokus = [[str((index//amount)+1)+str((index%amount)+1)+str(l) for index, l in enumerate(sudoku) if l != '.'] for sudoku in sudokus]
    cnf_files = ["\n".join(["p cnf %d %d" % (amount*amount*amount, len(sudoku)+len(sudoku))] + [l + ' 0' for l in sudoku] + rules) for sudoku in encoded_sudokus]
    return cnf_files



