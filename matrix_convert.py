import numpy as np
import copy

def print_as_matrix(Trues):
    if Trues == None:
        return None
    sorted = np.array(Trues)
    sorted = np.sort(sorted)
    if len(sorted) == 81:
        matrix = sorted.reshape((9,9))
        sudoku = check_position(matrix)
        sudoku = np.array(sudoku)
        sudoku = sudoku.reshape((9,9))
    elif len(sorted) == 16:
        matrix = sorted.reshape((4,4))
        sudoku = check_position(matrix)
        sudoku = np.array(sudoku)
        sudoku = sudoku.reshape((4,4))
    elif len(sorted) == 256:
        matrix = sorted.reshape((16,16))
        sudoku = check_position(matrix)
        sudoku = np.array(sudoku)
        sudoku = sudoku.reshape((16,167))
    else:
        print('unclear sudoku size with length ',len(sorted))
        return None
    print(matrix)
    print(sudoku)
    return sudoku


def check_position(m):
    sudoku = copy.deepcopy(m)
    for i in range(len(m)):
        x = i + 1
        for j in range(len(m[i])):
            y = j + 1
            if x == int(str(m[i][j])[:1]) and y == int(str(m[i][j])[1:2]):
                sudoku[i][j] = m[i][j] % 10
    return sudoku







