from math import sqrt

def load_cnfs(path):
    '''Given the game it will automatically pick the correct rules for the sudoku'''
    with open(path, "r") as file_:
        games = file_.read().splitlines()
    N = int(sqrt(len(games[0])))
    print(N)
    with open("./rules/sudoku-rules-"+str(N)+"x"+str(N)+".txt", "r") as file_:
        rules = file_.read().splitlines()[1:]
    print(rules)
    encGames = [[str((index//N)+1)+str((index%N)+1)+str(l) for index, l in enumerate(game) if l != '.'] for game in games]
    cnfs = ["\n".join(["p cnf %d %d" % (N*N*N, len(game)+len(rules))] + [l + ' 0' for l in game] + rules) for game in encGames]
    return cnfs



