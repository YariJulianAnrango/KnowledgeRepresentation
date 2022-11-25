def read_sudoku(file):
    if ".txt" in file or ".cnf" in file:
        with open(file, "r") as f:
            lines = f.read().splitlines()[1:]
    else:
        lines = file.split("\n")[1:]
    clauses = [line.replace("  ", " ").replace(" 0", "").split(" ") for line in lines]
    return clauses


